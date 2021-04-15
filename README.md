# ROB530_WN2021_Team13_Final_Project
Final project of ROB 530, Team 13

This repository contains the Python code modified based on the polex library, which accompanies the paper "Long-Term Urban Vehicle Localization Using Pole Landmarks Extracted from 3-D Lidar Scans" submitted to the European Conference on Mobile Robots. 

![Particle-Filter on NCLT Dataset](https://github.com/ckhdd/ROB530_WN2021_Team13_Final_Project/blob/python3_update/Localization/2013-01-10.gif)

![Global map](https://github.com/ckhdd/ROB530_WN2021_Team13_Final_Project/blob/python3_update/results/2012-01-15/globalmap_3_6_7.png)

![Estimated Trajectory](https://github.com/ckhdd/ROB530_WN2021_Team13_Final_Project/blob/python3_update/results/2012-01-15/2012-01-15_2021-04-13_04-00-27.png)
# Prerequisites and setting up environment
## Anaconda3

1. create a anaconda environment with python version=2.7 and activate it 
```bash
conda create -n py3 python=3.6 anaconda
conda activate py3
```
2. Install the following pakage with pip in anaconda and check if they are installed correctly
```bash
pip3 install numpy matplotlib open3d progressbar2 pyquaternion transforms3d scipy scikit-image networkx psutil torch future imageio pytest
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
For running the code with KITTI dataset, there are some additional dependancies:
```
pip3 install opencv-python kittipy arrow
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

3. Build ray-tracing and add new path to PYTHONPATH - clone it from our repo because we modified it to work with python3 and then build
```bash
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
## Modify the data path and session name in the datapreprocess.py and localizationnclt.py (see comments in these two files).
1. ```git clone https://github.com/ckhdd/ROB530_WN2021_Team13_Final_Project.git  ```
2. In datapreprocess.py, change variable 'datadir'(line 23) to the directory of your downloaded dataset
3. In datapreprocess.py, comment out the seesions(line 30-56) you are not using. (In the provided exaple, we are using '2013-01-10') 
4. In localizationnclt.py, replace '2021-03' in the variable 'localization_name_start'(line 31) to the yyyy-mm you are currently in.
5. In localizationnclt.py, change the session(line 503) you are currently work on.

## Run python file for localization on NCLT
```bash
python3 localizationnclt.py
```
## Modify the data path and session name in the kittidrives.py and kittipoles.py (see comments in these two files).
1. In kittidrives.py, uncomment sequences based on what data you're using
2. In kittipoles.py, modify 'dataset' path (line 21) with path to the directory containing kitti dataaset
3. In kittipoles.py, modidy 'result_dir' (line 22) with path the output directory. Output files will be written here.
4. In kittipoles.py, modify 'seq' (line 396) with index of the uncommented sequence in kittidrives.py

## Run python file for localization on KITTI
```bash
python3 kittipoles.py
```

