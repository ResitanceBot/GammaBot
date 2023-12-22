cmake_minimum_required(VERSION 3.0.2)
project(cnn_image_processing)

find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_package(
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
