from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.conditions import IfCondition

ARGS=[
    DeclareLaunchArgument(
        'ntrip',
        default_value='false',
        description='Enable NTRIP client',
    ),
    
    DeclareLaunchArgument(
        'eval',
        default_value='false',
        description='Enable evaluation node',
    ),
]

def generate_launch_description():
    
    gnss_config = PathJoinSubstitution(
        [FindPackageShare('ublox_gnss_demo_launch'), 'config', 'gnss.yaml']
    )
    
    return LaunchDescription(ARGS + [
        Node(
            package='ublox_gnss_ros',
            executable='ublox_gnss_node',
            name='ublox_gnss_node',
            output='screen',
            parameters=[gnss_config],
            remappings=[
                ('/fix', '/ublox/fix'),
                ('/nmea', '/ublox/nmea'),
            ],
        ),

        Node(
            condition=IfCondition(LaunchConfiguration('ntrip')),
            name='ntrip_client',
            package='ntrip_client',
            executable='ntrip_ros.py',
            parameters=[gnss_config],
            remappings=[
                ('/nmea', '/ublox/nmea'),
            ],
        ),  
        
        Node(
            condition=IfCondition(LaunchConfiguration('eval')),
            package='gnss_eval_ros',
            executable='gnss_eval',
            name='gnss_eval',
            output='screen',
            parameters=[gnss_config],
            remappings=[('/fix', '/ublox/fix')],
        ),
    ])