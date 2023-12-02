#!/bin/bash

while IFS="" read -r p || [ -n "$p" ]
do
  printf 'Installing %s dependency ...\n' "$p"
  sudo apt install ros-noetic-"${p//_/-}"
done < ros_pkg_list.txt

printf 'Setup process finished OK :D"