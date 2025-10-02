cmake_minimum_required(VERSION 3.10)

# Project name
project(lab1_patterns)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add the executable
add_executable(lab01 
main.cpp
Customer.cpp
Customer.h
Operator.cpp
Operator.h
Bill.cpp
Bill.h)