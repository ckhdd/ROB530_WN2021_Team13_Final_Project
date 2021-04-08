cmake_minimum_required(VERSION 3.1 FATAL_ERROR)

project(ray_tracing LANGUAGES CXX VERSION 0.1)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread -Wall -Wextra")

find_package(Catch2 REQUIRED)

set(PYTHON_EXECUTABLE /home/atishays/anaconda3/envs/projEnv/bin/python)
find_package(pybind11 REQUIRED)

pybind11_add_module(ray_tracing_python cpp/ray_tracing_python.cpp)

add_custom_command(TARGET ray_tracing_python POST_BUILD 
    COMMAND "${CMAKE_COMMAND}" -E copy 
        "${CMAKE_BINARY_DIR}/ray_tracing_python.cpython-38-x86_64-linux-gnu.so" 
        "${CMAKE_SOURCE_DIR}/python/raytracing/"
    COMMENT "Copying shared library to Python directory")

execute_process(
    COMMAND python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())" 
    OUTPUT_VARIABLE PYTHON_SITE_PACKAGES 
    OUTPUT_STRIP_TRAILING_WHITESPACE)

install(
    DIRECTORY python/raytracing
    DESTINATION ${PYTHON_SITE_PACKAGES})

