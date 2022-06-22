cmake_minimum_required(VERSION 3.17)
project(ipk_2)

set(CMAKE_CXX_STANDARD 14)

add_executable(ipk-sniffer main.cpp)
target_link_libraries(ipk-sniffer -lpcap)