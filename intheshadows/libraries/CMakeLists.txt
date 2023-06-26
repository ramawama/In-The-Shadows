cmake_minimum_required(VERSION 3.26)
project(pathing)

#set(CMAKE_C_COMPILER "/usr/bin/i686-w64-mingw32-gcc" CACHE PATH "" FORCE)
#set(CMAKE_CXX_COMPILER "/usr/bin/i686-w64-mingw32-g++" CACHE PATH "" FORCE)
set(CMAKE_CXX_STANDARD 17)

add_library(pathing SHARED library.cpp)
