cmake_minimum_required(VERSION 3.0.2)
project(cnn_image_processing)

find_package(catkin REQUIRED COMPONENTS
   roscpp
   rospy
   std_msgs
   message_generation
   geometry_msgs
)

add_message_files(
  FILES
  ArucoCornerCoordinates.msg
  ArucoDistOri.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
)

catkin_package(
  CATKIN_DEPENDS message_runtime
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
