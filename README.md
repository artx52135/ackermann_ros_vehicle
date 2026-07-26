## 1. Клонирование
```bash
cd ~/ros2_ws/src
git clone https://github.com/artx52135/ackermann_ros_vehicle.git
```

## 2. Сборка пакетов
```
colcon build --packages-select ackermann_vehicle_description ackermann_teleop
source install/setup.bash
```

## 3. Запуск имитационной модели в RViz2
```
ros2 launch ackermann_vehicle_description display.launch.py
rviz2
```

## 4. Запуск имитационной модели в Gazebo
```
ros2 launch ackermann_vehicle_description gazebo.launch.py
```

## 5. Запуск имитационной модели в Gazebo в тестовом мире
```
ros2 launch ackermann_vehicle_description gazebo.launch.py world:=./src/ackermann_vehicle_description/worlds/test_world.world
```

## 6. Управление имитационной модели с клавиатуры
```
# Терминал 2
ros2 run ackermann_teleop ackermann_steering
# Терминал 3
ros2 run ackermann_teleop keyboard_teleop
```
