
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    map_dir = LaunchConfiguration(
        'map',
        default=os.path.join(
            get_package_share_directory('tugbot_navigation2'),
            'map',
            'map.yaml'))

    param_file_name = 'navigation2.yaml'
    param_dir = LaunchConfiguration(
        'params_file',
        default=os.path.join(
            get_package_share_directory('tugbot_3d_navigation'),
            'config',
            param_file_name))

    nav2_launch_file_dir = os.path.join(get_package_share_directory('nav2_bringup'), 'launch')

    rviz_config_dir = os.path.join(
        get_package_share_directory('tugbot_3d_navigation'),
        'rviz',
        'nav2.rviz')

    return LaunchDescription([
        DeclareLaunchArgument(
            'map',
            default_value=map_dir,
            description='Full path to map file to load'),

        DeclareLaunchArgument(
            'params_file',
            default_value=param_dir,
            description='Full path to param file to load'),

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([nav2_launch_file_dir, '/bringup_launch.py']),
            launch_arguments={
                'map': map_dir,
                'use_sim_time': use_sim_time,
                'params_file': param_dir}.items(),
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen'),
        
        Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='pointcloud_to_laserscan',
            output='screen',
            parameters=[
                {'target_frame': 'base_link'},  # ターゲットフレーム
                {'transform_tolerance': 0.01},  # 変換の許容誤差
                {'min_height': 0.5},  # 最小高さ
                {'max_height': 1.5},  # 最大高さ
                {'angle_min': -1.57},  # 最小角度（ラジアン）
                {'angle_max': 1.57},  # 最大角度（ラジアン）
                {'angle_increment': 0.01},  # 角度の増分（ラジアン）
                {'scan_time': 0.1},  # スキャン時間（秒）
                {'range_min': 0.3},  # 最小範囲（メートル）
                {'range_max': 30.0},  # 最大範囲（メートル）
                {'use_inf': True},  # 無限遠を使用するかどうか
            ],
            remappings=[
                ('cloud_in', '/world/world_demo/model/tugbot/link/scan_omni/sensor/scan_omni/scan/points'),  # 入力PointCloud2トピック
                ('scan', 'scan')  # 出力LaserScanトピック
            ]
        )
    ])