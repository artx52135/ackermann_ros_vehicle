import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_path = get_package_share_directory('ackermann_vehicle_description')
    
    xacro_path = os.path.join(pkg_path, 'urdf', 'car.xacro')
    
    robot_description = Command(['xacro ', xacro_path])
    
    return LaunchDescription([
        # Запуск сервера Gazebo (без графики)
        ExecuteProcess(
            cmd=['gzserver', '--verbose', '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        ),
        # Запуск графического клиента Gazebo
        ExecuteProcess(
            cmd=['gzclient'],
            output='screen'
        ),
        # Публикация состояния робота
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen'
        ),
        # Спавн модели
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'car', '-topic', 'robot_description'],
            output='screen'
        )
    ])