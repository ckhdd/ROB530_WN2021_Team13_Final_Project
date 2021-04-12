# ROB530_WN2021_Team13_Final_Project
Final project of ROB 530, Team 13
![Particle-Filter on NCLT Dataset](https://github.com/ckhdd/ROB530_WN2021_Team13_Final_Project/blob/python3_update/Localization/2013-01-10.gif)

![Global map](https://github.com/ckhdd/ROB530_WN2021_Team13_Final_Project/blob/python3_update/results/2012-01-15/globalmap_3_6_7.png)

![Estimated Trajectory](https://github.com/ckhdd/ROB530_WN2021_Team13_Final_Project/blob/python3_update/results/2012-01-15/2012-01-15_2021-04-13_04-00-27.png)
# Prerequisites and setting up environment
## Anaconda3

1. create a anaconda environment with python version=2.7 and activate it 
```bash
conda create -n py27 python=2.7 anaconda
conda activate py27
```
2. Install the following pakage with pip in anaconda and check if they are installed correctly
```bash
pip2 install numpy matplotlib open3d-python progressbar2 pyquaternion transforms3d scipy scikit-image networkx psutil torch future imageio pytest
conda list
```
## Set up Linux environment
```bash
sudo apt-get update 
sudo apt-get install -y build-essential \
        python-dev \
        python-pip \
        libpython2.7-dev \
        python3-dev \
        python3-pip \
        python-tk \
        libgl1-mesa-glx \
        git \
        cmake
```
## Build libraries from sources 

1. Build Catch2
```bash
cd ~
mkdir library
cd  library && \
git clone --branch v2.x https://github.com/catchorg/Catch2.git && \
mkdir Catch2/build && \
cd Catch2/build && \
cmake .. && \
make -j8 && \
sudo make install
```

2. Build Pybind11
```bash
cd ~/library && \
git clone https://github.com/pybind/pybind11.git && \
mkdir pybind11/build && \
cd pybind11/build && \
cmake .. && \
make -j8 && \
sudo make install
```
3. Build ray-tracing and add new path to PYTHONPATH
```bash
cd ~/library && \
git clone https://github.com/acschaefer/ray_tracing.git && \
mkdir ray_tracing/build && \
cd ray_tracing/build && \
cmake .. && \
make -j8 && \
sudo make install
```
```bash
echo PYTHONPATH=$PYTHONPATH:/home/yourusername/library/ray_tracing/python >> ~/.bashrc
echo $PYTHONPATH
(you should see /home/yourusername/library/ray_tracing/python has been added to $PYTHONPATH)
```
## Modify the data path and session name in the pynclt.py and ncltpoles.py (see comments in these two files).
1. ```git clone https://github.com/ckhdd/ROB530_WN2021_Team13_Final_Project.git  ```
2. In pynclt.py, change variable 'datadir'(line 23) to the directory of your downloaded dataset
3. In pynclt.py, comment out the seesions(line 30-56) you are not using. (In the provided exaple, we are using '2013-01-10') 
4. In ncltpoles.py, replace '2021-03' in the variable 'localization_name_start'(line 31) to the yyyy-mm you are currently in.
5. In ncltpoles.py, change the session(line 503) you are currently work on.     

## Download and unzip the dataset 
```bash
python downloader.py --date="2013-01-10" --vel --gt --gt_cov --sen
cd sensor_data
tar xzf <sensors_data_file_name>
cd ..
cd velodyne_data
tar xzf <velodyne_data_file_name>
```
Change 2013-01-10 to download any dataset you want to work on.

## Run python file for localization
```bash
python localiztionnclt.py
```
