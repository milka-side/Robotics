"""Figure-8 path: two circles, first left (w>0), then right (w<0)."""
import time
import math

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry

from .diff_drive_math import twist_to_wheel_speeds

class Figure8Path(Node):
    def __init__(self):
        super().__init__('figure_8_path')

        self.declare_parameter("linear_speed", 0.3)
        self.declare_parameter("angular_speed", 0.3)
        self.declare_parameter("wheel_radius", 0.4)
        self.declare_parameter("wheel_separation", 1.2)
        self.declare_parameter("rate_hz", 20.0)
        self.declare_parameter("odom_topic", "/odom")

        odom_topic = self.get_parameter("odom_topic").value
        self.pub = self.create_publisher(TwistStamped, "/cmd_vel", 10)

        # Чекаємо на одометрію, щоб переконатися, що зв'язок з Gazebo є
        self.odom_sub = self.create_subscription(Odometry, odom_topic, self._odom_callback, 10)
        self.odom_received = False

        self.get_logger().info("Waiting for odometry...")
        while rclpy.ok() and not self.odom_received:
            rclpy.spin_once(self, timeout_sec=0.1)

        self.get_logger().info("Starting Figure-8 path")

        v = float(self.get_parameter("linear_speed").value)
        w_abs = float(self.get_parameter("angular_speed").value)
        dt = 1.0 / max(float(self.get_parameter("rate_hz").value), 1.0)

        # Розрахунок тривалості одного кола (додаємо 4% на компенсацію інерції)
        duration = (2.0 * math.pi / max(w_abs, 1e-6)) * 1.04
        duration_ns = int(duration * 1e9)

        # Список кутових швидкостей: спочатку вліво (+), потім вправо (-)
        for i, w in enumerate([w_abs, -w_abs], start=1):
            side = "left" if w > 0 else "right"
            self.get_logger().info(f"Circle {i}/2 ({side}, w={w:+.2f})")

            msg = TwistStamped()
            msg.header.frame_id = 'base_link'
            msg.twist.linear.x = v
            msg.twist.angular.z = w

            # ВАЖЛИВО: Беремо час початку СИМУЛЯЦІЇ для кожного кола
            start_time = self.get_clock().now()

            # Цикл руху для одного кола
            while rclpy.ok():
                current_time = self.get_clock().now()
                if (current_time - start_time).nanoseconds >= duration_ns:
                    break

                msg.header.stamp = current_time.to_msg()
                self.pub.publish(msg)
                rclpy.spin_once(self, timeout_sec=0.0)
                time.sleep(dt)

            self.get_logger().info(f"Circle {i} complete.")
            time.sleep(0.1) # Коротка пауза між колами

        # Зупинка
        self.pub.publish(TwistStamped())
        self.get_logger().info("Figure-8 complete!")

    def _odom_callback(self, msg: Odometry):
        self.odom_received = True

def main(args=None):
    rclpy.init(args=args)
    node = Figure8Path()
    node.destroy_node()
    rclpy.shutdown()
