cmake_minimum_required(VERSION 3.17)
project(s3s)

find_package(PythonLibs 3 REQUIRED)
MESSAGE("PYTHON PATH: ${PYTHON_INCLUDE_PATH}")
INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})
find_package(PythonInterp ${PYTHONLIBS_VERSION_STRING} REQUIRED)

message(STATUS "Python executable is ${PYTHON_EXECUTABLE}")
message("PYTHONLIBS_VERSION_STRING: ${PYTHONLIBS_VERSION_STRING}")

# ppybind11
include_directories(pybind11/include)
add_subdirectory(pybind11)

set(CMAKE_CXX_STANDARD 14)

#add_executable(s3s main.cpp s3s.h s3s.cpp cfg.h cfg.cpp funcC.h funcC.cpp weights.h weights.cpp s3sPy.cpp)

pybind11_add_module(s3spy s3sPy.cpp  s3s.h s3s.cpp cfg.h cfg.cpp funcC.h funcC.cpp weights.h weights.cpp s3sPy.cpp)

INSTALL(TARGETS s3spy COMPONENT Library DESTINATION "${PROJECT_SOURCE_DIR}/install")