import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

import xacro


def generate_launch_description():

    pkg_path = os.path.join(get_package_share_directory('holonomic'))
    xacro_file = os.path.join(pkg_path,'description','robot.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    rviz_config_path = os.path.join(pkg_path, 'rviz','default.rviz')
    launch_rsp_path = os.path.join(pkg_path, 'launch','rsp.launch.py')
    nav2_rviz_config_path = os.path.join(get_package_share_directory("nav2_bringup"), "rviz", "nav2_default_view.rviz")

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    launch_rsp_path
                )
    )	
    start_rviz2 = Node(package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', nav2_rviz_config_path]
    )
	
    start_joint_state_publisher_gui = Node(package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    robot_localization_node = Node(
       package='robot_localization',
       executable='ekf_node',
       name='ekf_filter_node',
       output='screen',
       parameters=[os.path.join(pkg_path, 'config/ekf.yaml'), {'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    launch_args = DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                            description='Flag to enable use_sim_time')
    
    map_odom_tf = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=["0", "0", "0", "0", "0", "0", "base_footprint", "base_link"]
    )

    return LaunchDescription([
        rsp,
        launch_args, 
        robot_localization_node,
        start_rviz2,
        map_odom_tf,
        start_joint_state_publisher_gui
    ])
