import warnings

import numpy as np
import scipy

import util


class particlefilter:
    def __init__(self, count, start, posrange, angrange, 
            polemeans, polevar, T_w_o=np.identity(4)):
        self.p_min = 0.01
        self.d_max = np.sqrt(-2.0 * polevar * np.log(
            np.sqrt(2.0 * np.pi * polevar) * self.p_min))
        self.minneff = 0.5
        self.estimatetype = 'best'
        self.count = count
        r = np.random.uniform(low=0.0, high=posrange, size=[self.count, 1])
        angle = np.random.uniform(low=-np.pi, high=np.pi, size=[self.count, 1])
        xy = r * np.hstack([np.cos(angle), np.sin(angle)])
        dxyp = np.hstack([xy, np.random.uniform(
            low=-angrange, high=angrange, size=[self.count, 1])])
        
        self.particles = np.matmul(start, util.xyp2ht(dxyp))
        self.xukf = np.zeros((3,1))
        self.particles_pre = np.matmul(start, util.xyp2ht(dxyp))
        self.Pukf = 0.2*np.ones((count,3,3))
        self.Poutt = np.ones((3,3))
        
        self.weights = np.full(self.count, 1.0 / self.count)
        self.polemeans = polemeans
        self.poledist = scipy.stats.norm(loc=0.0, scale=np.sqrt(polevar))
        self.kdtree = scipy.spatial.cKDTree(polemeans[:, :2], leafsize=3)
        self.T_w_o = T_w_o
        self.T_o_w = util.invert_ht(self.T_w_o)

    @property
    def neff(self):
        return 1.0 / (np.sum(self.weights**2.0) * self.count)

    def update_motion(self, mean, cov):
        T_r0_r1 = util.xyp2ht(
            np.random.multivariate_normal(mean, cov, self.count))
        self.particles = np.matmul(self.particles, T_r0_r1)
    def scaledSymmetricSigmaPoints(self, x, P):
        n = x.shape[0]
        nPts = 2*n + 1
        alpha = 1
        beta = 0
        kappa = 2
        kappa = alpha*alpha*(n + kappa) - n
        wPts = np.zeros((1,nPts));
        xPts =np.zeros((n,nPts));
        Psqrtm = np.linalg.cholesky((n+kappa)*P)
        xPts=np.hstack([np.zeros((P.shape[0],1)), -Psqrtm, Psqrtm]);
        xPts = xPts + np.tile(x.reshape(n,1),nPts)
        wPts=np.hstack([kappa,0.5*np.ones(nPts-1),0])/(n+kappa);
        wPts[nPts] = wPts[0] + (1-alpha*alpha) + beta;
        return xPts,wPts,nPts
    def measurement(self, X, poleparams):
        n = poleparams.shape[0]
        polepos_r = np.hstack(
            [poleparams[:, :2], np.zeros([n, 1]), np.ones([n, 1])]).T
        polepos_w = X.dot(polepos_r) # (3,Nout)
        d, ind = self.kdtree.query(polepos_w[:2].T, k=1, distance_upper_bound=self.d_max)
        
        Z = self.polemeans[:, :2][ind].reshape(-1,1) # (2*Nout,1)
        z_pred = polepos_w.T[:2].reshape(-1,1) # (2*Nout,1)
        return Z, z_pred
    def motion(self, Xin, mean, cov):
        T_r0_r1 = util.xyp2ht(np.random.multivariate_normal(mean, cov))
        return np.matmul(Xin, T_r0_r1)
    def update_motion_improved(self, mean, cov, poleparams):
        for i in range(self.count):
            x_out,Pout = self.ukf(self.particles_pre[i],self.Pukf[i,:,:], mean, cov, poleparams)
            x_new = x_out + np.random.multivariate_normal([0,0,0],Pout,1).T
            self.particles[i] = util.xyp2ht(x_new)
            self.Poutt = Pout
            self.xukf = x_out
            
    def update_measurement_improved(self, poleparams, resample=True):
        n = poleparams.shape[0]
        polepos_r = np.hstack(
            [poleparams[:, :2], np.zeros([n, 1]), np.ones([n, 1])]).T
        for i in range(self.count):
            polepos_w = self.particles[i].dot(polepos_r)
            d, _ = self.kdtree.query(polepos_w[:2].T, k=1, distance_upper_bound=self.d_max)
            lik = np.prod(self.poledist.pdf(np.clip(d, 0.0, self.d_max)) + 0.1)
            prior = scipy.stats.multivariate_normal(mean=[0,0,0], cov=self.Pukf[i,:,:]).pdf(util.ht2xyp(self.particles[i]) - util.ht2xyp(self.particles_pre[i]))
            proposal = scipy.stats.multivariate_normal(mean=[0,0,0], cov=self.Poutt).pdf(util.ht2xyp(self.particles[i]) - self.xukf)
            self.weights[i] *= lik*prior/proposal
            
            self.particles_pre[i] = self.particles[i].copy()
            self.Pukf[i,:,:] = self.Poutt.copy()
        self.weights /= np.sum(self.weights)
        if resample and self.neff < self.minneff:
            self.resample()
        
    def update_measurement(self, poleparams, resample=True):
        n = poleparams.shape[0]
        polepos_r = np.hstack(
            [poleparams[:, :2], np.zeros([n, 1]), np.ones([n, 1])]).T
        for i in range(self.count):
            polepos_w = self.particles[i].dot(polepos_r)
            d, _ = self.kdtree.query(
                polepos_w[:2].T, k=1, distance_upper_bound=self.d_max)
            self.weights[i] *= np.prod(
                self.poledist.pdf(np.clip(d, 0.0, self.d_max)) + 0.1)
        self.weights /= np.sum(self.weights)

        if resample and self.neff < self.minneff:
            self.resample()
    def ukf(self, Xin, Pin, mean, cov, poleparams):
        # Xin:matrix.
        Z, z_pred = self.measurement(Xin, poleparams)
        x_in = util.ht2xyp(Xin) #(3,)
        Qukf = 0.5 * np.eye(x_in.shape[0])
        Rukf = 0.01 * np.eye(z_pred.shape[0])
        states = x_in.shape[0] # 3
        observations = z_pred.shape[0] # 2*Nout
        vNoise = Qukf.shape[1]
        wNoise = Rukf.shape[1]
        noises = vNoise + wNoise
        if noises:
            N = scipy.linalg.block_diag(Qukf,Rukf)
            P_q = scipy.linalg.block_diag(Pin,N)
            x_q = np.vstack([x_in.reshape(-1,1), np.zeros((noises,1))])
        else:
            P_q = Pin
            x_q = x_in.reshape(-1,1)
        xSigmaPts, wSigmaPts, nsp = self.scaledSymmetricSigmaPoints(x_q, P_q)
        '''
            xSigmaPts (3+num_noise,nsp)
            wSigmaPts (nsp+1,)
        '''
        wSigmaPts_xmat = np.tile(wSigmaPts[1:nsp],(states,1)) # (3+num_noise,nsp-1)
        wSigmaPts_zmat = np.tile(wSigmaPts[1:nsp],(observations,1))
        xPredSigmaPts = np.zeros((states,nsp))
        zPredSigmaPts = np.zeros((states,nsp))
        for i in range (nsp):
            x_pred = self.motion(util.xyp2ht(xSigmaPts[:states,i].reshape(-1)), mean, cov) + xSigmaPts[states:states+vNoise,i]
            # xPredSigmaPts.append(util.ht2xyp(x_pred).reshape(3,1))
            xPredSigmaPts[:,i] = x_pred.reshape(states,1)
            z_pred = self.measurement(x_pred, poleparams) + xSigmaPts[states+vNoise:states+noises,i] #(2*Nout,1)
            # zPredSigmaPts.append(z_pred)
            zPredSigmaPts[:,i] = z_pred
        xPredSigmaPts = np.array(xPredSigmaPts) # (3,7)
        zPredSigmaPts = np.array(zPredSigmaPts) # (2*Nout,7)
        
        xPred = np.sum(wSigmaPts_xmat * (xPredSigmaPts[:,1:nsp] - np.tile(xPredSigmaPts[:,0],(1,nsp-1))), axis=1).reshape(-1,1) # (3,1)
        zPred = np.sum(wSigmaPts_zmat * (zPredSigmaPts[:,1:nsp] - np.tile(zPredSigmaPts[:,0],(1,nsp-1))), axis=1).reshape(-1,1) # (2*Nout,1)
        xPred = xPred + xPredSigmaPts[:,0]
        zPred = zPred + zPredSigmaPts[:,0]
        
        exSigmaPt = xPredSigmaPts[:,0] - xPred;
        ezSigmaPt = zPredSigmaPts[:,0] - zPred;
        
        PPred = wSigmaPts[nsp] * exSigmaPt.dot(exSigmaPt.T)
        PxzPred = wSigmaPts[nsp] * exSigmaPt.dot(ezSigmaPt.T)
        S = wSigmaPts[nsp] * ezSigmaPt.dot(ezSigmaPt.T)
        
        exSigmaPt = xPredSigmaPts[:,1:nsp] - np.tile(xPred,(1,nsp-1)) # (3,nsp-1)
        ezSigmaPt = zPredSigmaPts[:,1:nsp] - np.tile(zPred,(1,nsp-1)) # (2*Nout,nsp-1)
        PPred = PPred + (wSigmaPts_xmat * exSigmaPt).dot(exSigmaPt.T)
        S = S + (wSigmaPts_zmat * ezSigmaPt).dot(ezSigmaPt.T)
        PxzPred = PxzPred + exSigmaPt.dot((wSigmaPts_zmat * ezSigmaPt).T)
        
        K = PxzPred.dot(np.linalg.inv(S))
        inovation = Z - zPred
        Xout = xPred + K.dot(inovation)
        Pout = PPred - K @ S @ K.T
        return Xout, Pout

        



    def estimate_pose(self):
        if self.estimatetype == 'mean':
            xyp = util.ht2xyp(np.matmul(self.T_o_w, self.particles))
            mean = np.hstack(
                [np.average(xyp[:, :2], axis=0, weights=self.weights),
                    util.average_angles(xyp[:, 2], weights=self.weights)])
            return self.T_w_o.dot(util.xyp2ht(mean))
        if self.estimatetype == 'max':
            return self.particles[np.argmax(self.weights)]
        if self.estimatetype == 'best':
            i = np.argsort(self.weights)[-int(0.1 * self.count):]
            xyp = util.ht2xyp(np.matmul(self.T_o_w, self.particles[i]))
            mean = np.hstack(
                [np.average(xyp[:, :2], axis=0, weights=self.weights[i]),
                    util.average_angles(xyp[:, 2], weights=self.weights[i])])                
            return self.T_w_o.dot(util.xyp2ht(mean))

    def resample(self):
        cumsum = np.cumsum(self.weights)
        pos = np.random.rand() / self.count
        idx = np.empty(self.count, dtype=np.int)
        ics = 0
        for i in range(self.count):
            while cumsum[ics] < pos:
                ics += 1
            idx[i] = ics
            pos += 1.0 / self.count
        self.particles_pre = self.particles_pre[idx]
        self.Pukf = self.Pukf[idx]
        self.weights[:] = 1.0 / self.count
