#!/bin/bash

printf 'Starting scanning of dependencies, it could take some time ...\n\n'

while IFS="" read -r p || [ -n "$p" ]
do
  printf 'Installing %s dependency ...\n' "$p"
  sudo apt install -y ros-noetic-"${p//_/-}"
done < ros_pkg_list.txt

user_name=$(whoami)
if [ "$user_name" != "husarion" ]; then
  # For dev environment, next libraries are neccesary to achieve a correct compilation
  sudo apt install -y ros-noetic-libuvc-camera
  sudo apt install -y ros-noetic-libuvc-camera-dbgsym
  sudo apt install -y ros-noetic-libuvc-ros
  sudo apt install -y libgoogle-glog-dev
fi 

printf '\n\nSetup process finished OK :D\n\n'
