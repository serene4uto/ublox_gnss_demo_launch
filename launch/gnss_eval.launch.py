from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.conditions import IfCondition

ARGS=[
    DeclareLaunchArgument(
        'gt_lat',
        default_value='0.0',
        description='Ground truth latitude',
    ),
    DeclareLaunchArgument(
        'gt_lon',
        default_value='0.0',
        description='Ground truth longitude',
    ),
    DeclareLaunchArgument(
        'gt_alt',
        default_value='0.0',
        description='Ground truth altitude',
    ),
    DeclareLaunchArgument(
        'log_enable',
        default_value='true',
        description='Enable logging',
    ),
    DeclareLaunchArgument(
        'log_path',
        default_value='gnss_eval_log',
        description='Path to log file',
    ),
    DeclareLaunchArgument(
        'log_frequency',
        default_value='10',
        description='Log frequency (Hz)',
    ),
    DeclareLaunchArgument(
        'rate_window_size',
        default_value='50',
        description='Size of window for rate calculation',
    ),
]

def generate_launch_description():
    
    return LaunchDescription(ARGS + [        
        Node(
            package='gnss_utils_ros',
            executable='gnss_eval',
            name='gnss_eval',
            output='screen',
            parameters=[
                {
                    'ground_truth.latitude': LaunchConfiguration('gt_lat'),
                    'ground_truth.longitude': LaunchConfiguration('gt_lon'),
                    'ground_truth.altitude': LaunchConfiguration('gt_alt'),
                    'log_enable': LaunchConfiguration('log_enable'),
                    'log_path': LaunchConfiguration('log_path'),
                    'log_frequency': LaunchConfiguration('log_frequency'),
                    'rate_window_size': LaunchConfiguration('rate_window_size'),
                }
            ],
            remappings=[
                ('/fix', '/ublox/fix')
            ],
        ),
    ])