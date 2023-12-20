cmake_minimum_required(VERSION 3.0.2)
project(gamepad_control)

find_package(catkin REQUIRED COMPONENTS
  joy
  roscpp
  rospy
  std_msgs
)

catkin_package(
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(joy_to_cmd_vel src/joy_to_cmd_vel.cpp)
target_link_libraries(joy_to_cmd_vel ${catkin_LIBRARIES})
