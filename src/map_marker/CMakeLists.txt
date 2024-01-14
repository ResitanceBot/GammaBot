cmake_minimum_required(VERSION 3.0.2)
project(map_marker)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  cnn_image_processing
  message_generation
  geometry_msgs
  tf
)

generate_messages(
  DEPENDENCIES
  cnn_image_processing
  std_msgs
  geometry_msgs
)

catkin_package(
  CATKIN_DEPENDS 
  cnn_image_processing
  message_runtime
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(map_marker src/map_marker.cpp)
target_link_libraries(map_marker ${catkin_LIBRARIES})
