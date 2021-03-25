# ROB530_WN2021_Team13_Final_Project
Final project of ROB 530, Team 13
![Particle-Filter on NCLT Dataset](https://github.com/ckhdd/ROB530_WN2021_Team13_Final_Project/blob/main/Localization/2013-01-10.gif)
# Pre-requists and setting up environment
Anaconda3
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
3. Set up Linux environment
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
4. Build libraries from sources 
(1) Build Catch2
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

(2) Build Pybind11
```bash
cd ~/library && \
git clone https://github.com/pybind/pybind11.git && \
mkdir pybind11/build && \
cd pybind11/build && \
cmake .. && \
make -j8 && \
sudo make install
```
(3) Build ray-tracing and add new path to PYTHONPATH
```bash
cd ~/library && \
git clone https://github.com/acschaefer/ray_tracing.git && \
mkdir ray_tracing/build && \
cd ray_tracing/build && \
cmake .. && \
make -j8 && \
sudo make install
echo PYTHONPATH=$PYTHONPATH:/home/yourusername/library/ray_tracing/python >> ~/.bashrc
```
