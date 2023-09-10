#!/bin/bash

map_name="map"

if [ "$1" ]; then
  map_name=$1
fi

# map_saverを実行して地図を保存
ros2 run nav2_map_server map_saver_cli -f ../map/$map_name
