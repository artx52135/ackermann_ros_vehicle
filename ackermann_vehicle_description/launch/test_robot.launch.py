import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_path = get_package_share_directory('ackermann_vehicle_description')
    
    # Путь к тестовому URDF (не xacro!)
    urdf_file = os.path.join(pkg_path, 'urdf', 'test_robot.urdf')
    
    # Читаем URDF файл
    with open(urdf_file, 'r') as f:
        robot_description_content = f.read()
    
    robot_description = {'robot_description': robot_description_content}
    
    # Запуск Gazebo
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
            '-entity', 'test_robot', 
            '-topic', 'robot_description', 
            '-x', '0', 
            '-y', '0', 
            '-z', '0.2'
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