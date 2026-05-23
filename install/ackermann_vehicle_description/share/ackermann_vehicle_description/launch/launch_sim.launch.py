import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'ackermann_vehicle_description'
    
    # Путь к rsp launch файлу
    rsp_launch_path = os.path.join(
        get_package_share_directory(package_name),
        'launch',
        'rsp.launch.py'
    )
    
    # Запуск rsp (robot_state_publisher)
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(rsp_launch_path),
        launch_arguments={'use_sim_time': 'true'}.items()
    )
    
    # Запуск Gazebo
    gazebo_launch_path = os.path.join(
        get_package_share_directory('gazebo_ros'),
        'launch',
        'gazebo.launch.py'
    )
    
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_path),
        launch_arguments={'verbose': 'true'}.items()
    )
    
    # Спавн машины
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'car',
            '-x', '0',
            '-y', '0',
            '-z', '0.1'
        ],
        output='screen'
    )
    
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
    ])