import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from ament_index_python import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    sim_path = os.path.join(get_package_share_directory("holonomic"), "launch", "launch_sim.launch.py")
    rviz_path = os.path.join(get_package_share_directory("holonomic"), "launch", "rviz.launch.py")

    sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            sim_path
        )
    )

    rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            rviz_path
        )
    )

    return LaunchDescription([
        sim, rviz
    ])