import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    config = os.path.join(
        get_package_share_directory("moj_zolw"), "config", "prostokat.yaml"
    )

    return LaunchDescription(
        [
            Node(
                package="turtlesim",
                executable="turtlesim_node",
                name="turtlesim",
            ),
            Node(
                package="moj_zolw",
                executable="do_celu",
                name="do_celu",
                parameters=[config],
                output="screen",
            ),
        ]
    )
