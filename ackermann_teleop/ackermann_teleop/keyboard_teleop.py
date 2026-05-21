#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import termios
import tty
import select
import threading

class KeyboardTeleop(Node):
    def __init__(self):
        super().__init__('keyboard_teleop')
        
        # Публикуем в тему cmd_vel
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Параметры управления
        self.declare_parameter('linear_vel', 1.0)
        self.declare_parameter('angular_vel', 1.0)
        
        self.max_linear_vel = self.get_parameter('linear_vel').value
        self.max_angular_vel = self.get_parameter('angular_vel').value
        
        self.speed = 0.0
        self.turn = 0.0
        self.running = True
        
        self.get_logger().info('Keyboard Teleop Node Started')
        self.get_logger().info('Controls:')
        self.get_logger().info('  w/s - forward/backward')
        self.get_logger().info('  a/d - turn left/right')
        self.get_logger().info('  q - increase speed limit')
        self.get_logger().info('  e - decrease speed limit')
        self.get_logger().info('  x - stop')
        self.get_logger().info('  Ctrl+C - exit')
        
    def get_key(self):
        try:
            tty.setraw(sys.stdin.fileno())
            select.select([sys.stdin], [], [], 0)
            key = sys.stdin.read(1)
            return key
        except:
            return ''
            
    def keyboard_loop(self):
        # Сохраняем настройки терминала
        old_settings = termios.tcgetattr(sys.stdin)
        
        linear_step = 0.1
        angular_step = 0.2
        
        try:
            while self.running and rclpy.ok():
                key = self.get_key()
                
                if key == 'w':
                    self.speed = min(self.speed + linear_step, self.max_linear_vel)
                    self.get_logger().info(f'Forward: speed={self.speed:.2f}')
                elif key == 's':
                    self.speed = max(self.speed - linear_step, -self.max_linear_vel)
                    self.get_logger().info(f'Backward: speed={self.speed:.2f}')
                elif key == 'a':
                    self.turn = min(self.turn + angular_step, self.max_angular_vel)
                    self.get_logger().info(f'Turn Left: angle={self.turn:.2f}')
                elif key == 'd':
                    self.turn = max(self.turn - angular_step, -self.max_angular_vel)
                    self.get_logger().info(f'Turn Right: angle={self.turn:.2f}')
                elif key == 'q':
                    self.max_linear_vel = min(self.max_linear_vel + 0.2, 3.0)
                    self.max_angular_vel = min(self.max_angular_vel + 0.2, 2.0)
                    self.get_logger().info(f'Max speed increased: linear={self.max_linear_vel:.2f}, angular={self.max_angular_vel:.2f}')
                elif key == 'e':
                    self.max_linear_vel = max(self.max_linear_vel - 0.2, 0.2)
                    self.max_angular_vel = max(self.max_angular_vel - 0.2, 0.2)
                    self.get_logger().info(f'Max speed decreased: linear={self.max_linear_vel:.2f}, angular={self.max_angular_vel:.2f}')
                elif key == 'x':
                    self.speed = 0.0
                    self.turn = 0.0
                    self.get_logger().info('Stop')
                elif key == '\x03':  # Ctrl+C
                    self.running = False
                    break
                
                # Создаем и публикуем сообщение Twist
                twist_msg = Twist()
                twist_msg.linear.x = self.speed
                twist_msg.angular.z = self.turn
                self.publisher.publish(twist_msg)
                
        except Exception as e:
            self.get_logger().error(f'Error in keyboard loop: {e}')
        finally:
            # Восстанавливаем настройки терминала
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            self.get_logger().info('Keyboard teleop stopped')
    
    def run(self):
        # Запускаем клавиатурный ввод в отдельном потоке
        keyboard_thread = threading.Thread(target=self.keyboard_loop)
        keyboard_thread.daemon = True
        keyboard_thread.start()
        
        # Держим ноду активной
        while self.running and rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.1)
        
        keyboard_thread.join(timeout=1.0)

def main(args=None):
    rclpy.init(args=args)
    node = KeyboardTeleop()
    
    try:
        node.run()
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down keyboard teleop...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()