import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class Rysownik(Node):
    def __init__(self):
        super().__init__("rysownik")
        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.licznik = 0
        self.get_logger().info("Rysownik uruchomiony!")

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.0
        self.publisher.publish(msg)
        self.licznik += 1
        self.get_logger().info(f"Wysłano polecenie nr {self.licznik}")


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
