from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    urdf_path = os.path.join(get_package_share_directory('tugbot_description'), 'urdf', 'model.urdf')

    return LaunchDescription([
        DeclareLaunchArgument(
            'urdf_file',
            default_value=urdf_path,
            description='Full path to the URDF file to load'
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            arguments=[LaunchConfiguration('urdf_file')],
            output='screen'
        )
    ])
