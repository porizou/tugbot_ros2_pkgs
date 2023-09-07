from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import LogInfo, ExecuteProcess


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
            ('/scan', '/scan'),
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
    
    pointcloud_to_laserscan = Node(
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
    
    teleop_twist_keyboard_node = ExecuteProcess(
        cmd=['gnome-terminal', '--', 'ros2', 'run', 'teleop_twist_keyboard', 'teleop_twist_keyboard'],
        shell=False,
        output='screen'
    )
    
    ld = LaunchDescription()
    ld.add_action(slam_node)
    ld.add_action(rviz2_node)
    ld.add_action(pointcloud_to_laserscan)
    ld.add_action(LogInfo(msg="Opening a new terminal window for teleop_twist_keyboard..."))
    ld.add_action(teleop_twist_keyboard_node)
    return ld