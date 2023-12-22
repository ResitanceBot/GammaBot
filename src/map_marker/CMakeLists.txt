cmake_minimum_required(VERSION 3.0.2)
project(map_marker)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
)

catkin_package(
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(map_marker src/map_marker.cpp)
target_link_libraries(map_marker ${catkin_LIBRARIES})
