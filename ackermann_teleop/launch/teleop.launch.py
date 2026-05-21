from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ackermann_teleop',
            executable='keyboard_teleop',
            name='keyboard_teleop',
            output='screen',
            emulate_tty=True
        )
    ])