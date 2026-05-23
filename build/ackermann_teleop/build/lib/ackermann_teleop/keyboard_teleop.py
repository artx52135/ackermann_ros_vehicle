#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import termios
import tty
import sys
import select

class KeyboardTeleop(Node):
    def __init__(self):
        super().__init__('keyboard_teleop')
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        
        self.settings = termios.tcgetattr(sys.stdin)
        
        # НАСТРОЙКИ СКОРОСТЕЙ
        self.forward_speed = 0.3    # Медленно вперёд (было 0.5)
        self.backward_speed = -0.3  # Медленно назад (было -0.5)
        self.turn_speed = 2.0       # Резкий поворот (было 1.2)
        
        self.moving_forward = False
        self.moving_backward = False
        self.turning_left = False
        self.turning_right = False
        
        print('''
╔════════════════════════════════════════════════╗
║         KEYBOARD TELEOP                        ║
╠════════════════════════════════════════════════╣
║  I  - Вперёд (МЕДЛЕННО)                       ║
║  K  - Стоп                                     ║
║  ,  - Назад (МЕДЛЕННО)                        ║
║  J  - Поворот налево (РЕЗКО)                  ║
║  L  - Поворот направо (РЕЗКО)                 ║
║  +/- - Увеличить/уменьшить скорость           ║
║  Q   - Выход                                   ║
╠════════════════════════════════════════════════╣
║  Текущие скорости:                            ║
║  Вперёд/Назад: 0.3 м/с                        ║
║  Поворот: 2.0 рад/с                           ║
╚════════════════════════════════════════════════╝
''')
    
    def get_key(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.05)
        key = sys.stdin.read(1) if rlist else None
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key
    
    def run(self):
        try:
            while rclpy.ok():
                key = self.get_key()
                msg = Twist()
                
                if key == 'i':
                    self.moving_forward = True
                    self.moving_backward = False
                    self.turning_left = False
                    self.turning_right = False
                    msg.linear.x = self.forward_speed
                    msg.angular.z = 0.0
                    print(f'ВПЕРЁД ({self.forward_speed:.1f} м/с)')
                
                elif key == ',':
                    self.moving_forward = False
                    self.moving_backward = True
                    self.turning_left = False
                    self.turning_right = False
                    msg.linear.x = self.backward_speed
                    msg.angular.z = 0.0
                    print(f'НАЗАД ({abs(self.backward_speed):.1f} м/с)')
                
                elif key == 'j':
                    self.moving_forward = False
                    self.moving_backward = False
                    self.turning_left = True
                    self.turning_right = False
                    msg.linear.x = 0.0
                    msg.angular.z = self.turn_speed
                    print(f'ПОВОРОТ НАЛЕВО (РЕЗКО)')
                
                elif key == 'l':
                    self.moving_forward = False
                    self.moving_backward = False
                    self.turning_left = False
                    self.turning_right = True
                    msg.linear.x = 0.0
                    msg.angular.z = -self.turn_speed
                    print(f'ПОВОРОТ НАПРАВО (РЕЗКО)')
                
                elif key == 'k' or key == ' ':
                    self.moving_forward = False
                    self.moving_backward = False
                    self.turning_left = False
                    self.turning_right = False
                    msg.linear.x = 0.0
                    msg.angular.z = 0.0
                    print('СТОП')
                
                elif key == '+':
                    self.forward_speed = min(self.forward_speed + 0.1, 1.0)
                    self.backward_speed = -self.forward_speed
                    self.turn_speed = min(self.turn_speed + 0.2, 3.0)
                    print(f'СКОРОСТЬ: Вперёд={self.forward_speed:.1f}, Поворот={self.turn_speed:.1f}')
                
                elif key == '-':
                    self.forward_speed = max(self.forward_speed - 0.1, 0.2)
                    self.backward_speed = -self.forward_speed
                    self.turn_speed = max(self.turn_speed - 0.2, 1.0)
                    print(f'СКОРОСТЬ: Вперёд={self.forward_speed:.1f}, Поворот={self.turn_speed:.1f}')
                
                elif key == 'q':
                    break
                
                elif self.moving_forward:
                    msg.linear.x = self.forward_speed
                elif self.moving_backward:
                    msg.linear.x = self.backward_speed
                elif self.turning_left:
                    msg.angular.z = self.turn_speed
                elif self.turning_right:
                    msg.angular.z = -self.turn_speed
                else:
                    continue
                
                self.pub.publish(msg)
                
        except Exception as e:
            print(f'Error: {e}')
        finally:
            msg = Twist()
            self.pub.publish(msg)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)

def main(args=None):
    rclpy.init(args=args)
    teleop = KeyboardTeleop()
    teleop.run()
    teleop.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()