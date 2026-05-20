cmake_minimum_required(VERSION 3.8)
project(ackermann_vehicle_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(xacro REQUIRED)

# Установка всех файлов meshes (включая .dae, .png)
install(DIRECTORY meshes
  DESTINATION share/${PROJECT_NAME}
  PATTERN ".git" EXCLUDE
)

# Установка urdf файлов
install(DIRECTORY urdf
  DESTINATION share/${PROJECT_NAME}
  PATTERN ".git" EXCLUDE
)

# Установка materials если есть
install(DIRECTORY materials
  DESTINATION share/${PROJECT_NAME}
  OPTIONAL
  PATTERN ".git" EXCLUDE
)

# Установка launch файлов
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
  OPTIONAL
  PATTERN "*.launch" EXCLUDE
  PATTERN ".git" EXCLUDE
)

ament_package()
