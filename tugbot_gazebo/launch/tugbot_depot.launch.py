from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    world_file_path = PathJoinSubstitution([
        get_package_share_directory('tugbot_gazebo'),
        'worlds',
        'tugbot_depot.sdf'
    ])

    ign_ros_bridge_launch_path = PathJoinSubstitution([
        get_package_share_directory('tugbot_gazebo'),
        'launch',
        'ign_ros2_bridge.launch.py'
    ])
    
    robot_description_launch_path = PathJoinSubstitution([
        get_package_share_directory('tugbot_description'),
        'launch',
        'tugbot_description.launch.py'
    ])

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('ros_gz_sim'), 'launch'), '/gz_sim.launch.py']),
            launch_arguments=[
                ('gz_args', world_file_path)]
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(ign_ros_bridge_launch_path)
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(robot_description_launch_path)
        )
    ])
