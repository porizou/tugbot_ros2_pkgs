from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    slam_node = Node(
        package='slam_toolbox', executable='sync_slam_toolbox_node',
        output='screen',
        parameters=[
            get_package_share_directory(
                'tugbot_slam')
            + '/config/mapper_params_offline.yaml'
        ],
        remappings=[
            ('/scan', '/world/world_demo/model/tugbot/link/scan_front/sensor/scan_front/scan'),
        ],
    )

    rviz2_node = Node(
        name='rviz2',
        package='rviz2', executable='rviz2', output='screen',
        arguments=[
            '-d',
            get_package_share_directory('tugbot_slam')
            + '/rviz/default.rviz'],
    )
    
    ld = LaunchDescription()
    ld.add_action(slam_node)
    ld.add_action(rviz2_node)

    return ld