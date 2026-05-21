import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro

def generate_launch_description():
    pkg_path = get_package_share_directory('ackermann_vehicle_description')
    
    # Конвертация xacro в urdf
    xacro_file = os.path.join(pkg_path, 'urdf', 'car.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_description = {'robot_description': robot_description_config.toxml()}
    
    # Запуск Gazebo с пустым миром
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ]),
        launch_arguments={'verbose': 'false'}.items()
    )
    
    # Спавн робота
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'car', 
            '-topic', 'robot_description', 
            '-x', '0', 
            '-y', '0', 
            '-z', '0.1'
        ],
        output='screen'
    )
    
    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description, {'use_sim_time': True}]
    )
    
    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_entity,
    ])