# ray_tracing

Fast grid-based ray tracing in C++ and Python

## What is `ray_tracing`?

This library implements ray tracing through a uniform grid according to the algorithm proposed by Amanatides and Woo:

> [Amanatides, John, and Andrew Woo.](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.42.3443&rep=rep1&type=pdf)<br/>
> [**A fast voxel traversal algorithm for ray tracing.**](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.42.3443&rep=rep1&type=pdf)<br/>
> [*Eurographics. Vol. 87. No. 3. 1987.*](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.42.3443&rep=rep1&type=pdf)

The `ray_tracing` library is written in C++.
In addition, it comes with Python bindings via [pybind11](https://pybind11.readthedocs.io/en/stable/).

## How to use `ray_tracing`?

1. Install the required dependencies Catch2, pytest, and pybind11.

   ```bash
    git clone https://github.com/catchorg/Catch2.git
    mkdir Catch2/build
    cd Catch2/build
    cmake ..
    make -j8
    sudo make install

    pip install pytest

    git clone https://github.com/pybind/pybind11.git
    mkdir pybind11/build
    cd pybind11/build
    cmake ..
    make -j8
    sudo make install
    ```

2. Depends on the python version you are using, you will have to modify the CMakeLists.txt 

   (1) Change PYTHON_EXECUTABLE to the path that the python you are using locates. For example, we create a python3.6 environment named py36 via anaconda3 in Unbuntu 16.04 for the test and we set the PYTHON_EXECUTABLE as the following
   ``` /home/youusername/anaconda3/envs/py36/bin/python ```
   
   (2) Change ``${CMAKE_BINARY_DIR}`` to the file name of .so binary file corresponding to your python version, for example, `ray_tracing_python.cpython-36m-x86_64-linux-gnu.so` for python 3.6.10, `ray_tracing_python.cpython-38-x86_64-linux-gnu.so` for python 3.8.5.

3. Compile the repository.
  
    ```bash
    mkdir ray_tracing/build && cd ray_tracing/build
    cmake ..
    make -j8
    sudo make install
    ```

