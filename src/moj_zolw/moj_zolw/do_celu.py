import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim_msgs.msg import Pose


class DoCelu(Node):
    def __init__(self):
        super().__init__("do_celu")
        self.ruchy = 0
        self.declare_parameter("cel_x", 0.0)
        self.declare_parameter("cel_y", 0.0)
        self.declare_parameter("dlugosc_x", 0.0)
        self.declare_parameter("dlugosc_y", 0.0)
        self.cel_x = self.get_parameter("cel_x").value
        self.cel_y = self.get_parameter("cel_y").value
        self.dlugosc_x = self.get_parameter("dlugosc_x").value
        self.dlugosc_y = self.get_parameter("dlugosc_y").value
        x0, y0 = self.cel_x, self.cel_y
        dx, dy = self.dlugosc_x, self.dlugosc_y
        self.punkty = [
            (x0, y0),
            (x0 + dx, y0),
            (x0 + dx, y0 + dy),
            (x0, y0 + dy),
            (x0, y0),
        ]
        self.pose = None  # jeszcze nie wiemy, gdzie jest żółw

        self.publisher = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.subscription = self.create_subscription(
            Pose, "/turtle1/pose", self.pose_callback, 10
        )
        self.timer = self.create_timer(0.1, self.sterowanie)

        self.get_logger().info(f"Jadę do celu ({self.cel_x}, {self.cel_y})")

    def pose_callback(self, msg):
        """Tylko zapamiętuje najnowszą pozycję."""
        self.pose = msg

    def sterowanie(self):
        """Pętla sterowania: zmierz → policz błąd → popraw ruch."""
        if self.pose is None or self.ruchy >= len(self.punkty):
            return
        cel_x, cel_y = self.punkty[self.ruchy]
        dx = cel_x - self.pose.x
        dy = cel_y - self.pose.y
        odleglosc = math.hypot(dx, dy)

        # 2. Jesteśmy na miejscu?
        if odleglosc < 0.05:
            self.get_logger().info(f"Punkt: ({self.ruchy} / {len(self.punkty) - 1}")
            self.ruchy += 1
            if self.ruchy >= len(self.punkty):
                self.publisher.publish(Twist())  # pusty Twist = stop
                self.timer.cancel()
                self.get_logger().info(
                    f"Cel osiągnięty! Pozycja: ({self.pose.x:.2f}, {self.pose.y:.2f})"
                )
            return

        # 3. W którą stronę obrócić?
        kat_do_celu = math.atan2(dy, dx)
        blad_kata = kat_do_celu - self.pose.theta
        blad_kata = math.atan2(math.sin(blad_kata), math.cos(blad_kata))

        # 4. Polecenie ruchu
        msg = Twist()
        msg.angular.z = 1.5 * blad_kata
        if abs(blad_kata) < 0.05:  # jedź do przodu tylko gdy patrzysz w stronę celu
            msg.linear.x = min(1.5 * odleglosc, 2.0) * max(math.cos(blad_kata), 0.0)
        self.publisher.publish(msg)

        self.get_logger().info(
            f"odległość: {odleglosc:.2f}, błąd kąta: {blad_kata:.2f}",
            throttle_duration_sec=1.0,
        )


def main(args=None):
    rclpy.init(args=args)
    node = DoCelu()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
