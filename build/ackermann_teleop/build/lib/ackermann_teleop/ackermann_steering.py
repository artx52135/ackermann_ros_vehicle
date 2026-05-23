#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import math

class AckermannSteering(Node):
    def __init__(self):
        super().__init__('ackermann_steering')
        
        self.sub = self.create_subscription(Twist, 'cmd_vel', self.cmd_callback, 10)
        # Новые имена joint'ов
        self.left_pub = self.create_publisher(Float64, '/front_left_steering_joint/cmd_pos', 10)
        self.right_pub = self.create_publisher(Float64, '/front_right_steering_joint/cmd_pos', 10)
        
        self.max_steering = 0.6
        self.current_angle = 0.0
        self.smoothing = 0.3
        
        self.get_logger().info('Ackermann Steering - ОБА КОЛЕСА ПОВОРАЧИВАЮТСЯ ОДИНАКОВО')
    
    def cmd_callback(self, msg):
        angular = msg.angular.z
        
        target_angle = angular * 0.5
        target_angle = max(-self.max_steering, min(self.max_steering, target_angle))
        
        self.current_angle += (target_angle - self.current_angle) * self.smoothing
        
        self.left_pub.publish(Float64(data=self.current_angle))
        self.right_pub.publish(Float64(data=self.current_angle))
        
        if abs(angular) > 0.05:
            deg = math.degrees(self.current_angle)
            self.get_logger().info(f'Поворот колёс: {deg:.0f}°')

def main(args=None):
    rclpy.init(args=args)
    node = AckermannSteering()
    rclpy.spin(node)

if __name__ == '__main__':
    main()