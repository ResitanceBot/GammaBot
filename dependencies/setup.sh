#!/bin/bash

printf 'Starting scanning of dependencies, it could take some time ...\n\n'

while IFS="" read -r p || [ -n "$p" ]
do
  printf 'Installing %s dependency ...\n' "$p"
  sudo apt install -y ros-noetic-"${p//_/-}"
done < ros_pkg_list.txt

printf 'Setup process finished OK :D\n\n'
