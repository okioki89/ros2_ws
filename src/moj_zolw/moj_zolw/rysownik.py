import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class Rysownik(Node):
    def __init__(self):
        super().__init__("rysownik")
        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.licznik = 0
        self.get_logger().info("Rysownik uruchomiony!")

    def timer_callback(self):
        msg = Twist()
        if self.licznik < 8:
            if self.licznik % 2 == 0:
                msg.linear.x = 2.0
                msg.angular.z = 0.0
                self.get_logger().info(f"Krok: {self.licznik}, wykonano ruch")
            else:
                msg.linear.x = 0.0
                msg.angular.z = math.pi / 2
                self.get_logger().info(f"Krok: {self.licznik}, wykonano skret")

            self.publisher.publish(msg)
            self.licznik += 1
        else:
            self.timer.cancel()
            self.get_logger().info(f"Skończono kwadrat")


def main(args=None):
    rclpy.init(args=args)
    node = Rysownik()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
