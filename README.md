# tugbot_ros2_pkgs

## Overview

The `tugbot_ros2_pkgs` package is designed to enable the Tugbot robot to run in a ROS 2 environment using Ignition Gazebo. This package provides the necessary launch files, configurations, and dependencies to get Tugbot up and running seamlessly.

## Features

- **SLAM Integration**: Utilizes SLAM Toolbox for mapping and localization.
- **Teleoperation**: Includes teleoperation via keyboard.
- **Sensor Data Conversion**: Converts PointCloud2 data to LaserScan for compatibility with navigation packages.
- **Navigation**: Integrated with ROS 2 Navigation Stack (Nav2) for autonomous navigation.

## Prerequisites

- ROS 2 (Tested on Foxy, Galactic, and Humble)
- Ignition Gazebo
- Python 3.x

## Installation

1. Clone the repository into your ROS 2 workspace:

    ```bash
    git clone https://github.com/yourusername/tugbot_ros2_pkgs.git
    ```

2. Navigate to your ROS 2 workspace and build the package:

    ```bash
    cd ~/ros2_ws
    colcon build --packages-select tugbot_ros2_pkgs
    ```

3. Source your workspace:

    ```bash
    source ~/ros2_ws/install/setup.bash
    ```

## Run Ignition Gazebo world

```bash
ros2 launch tugbot_gazebo tugbot_depot.launch.py 
```

![image](https://github.com/porizou/tugbot_ros2_pkgs/assets/14184141/42029326-e426-4526-b185-4089b6a24416)

    
