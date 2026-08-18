from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    namespace = "jackal1"
    params_file = "/home/administrator/nahl_ws/real_jackal/config/new_nav2_params.yaml"
    #params_file = "/home/administrator/nahl_ws/real_jackal/config/old_physical.yaml"
    #map = "/home/administrator/nahl_ws/maps/robohub.yaml"
    map = "/home/administrator/nahl_ws/airlab.yaml"
    return LaunchDescription([
        # Map Server
        Node(
            package="nav2_map_server",
            executable="map_server",
            name="map_server",
            namespace=namespace,
            output="screen",
            parameters=[{"yaml_filename": map}],
            remappings=[
                ("/tf", "/jackal1/tf"),      
                ("/tf_static", "/jackal1/tf_static"),
            ],
        ),

        # AMCL
        Node(
            package="nav2_amcl",
            executable="amcl",
            name="amcl",
            namespace=namespace,
            output="screen",
            parameters=[params_file,{"use_sim_time": False}],
            remappings=[
                ("scan", "sensors/lidar3d_0/scan"), 
                ("odom", "platform/odom/filtered"), 
                ("/tf", "/jackal1/tf"),      
                ("/tf_static", "/jackal1/tf_static"),
            ],
        ),

        # Planner Server
        Node(
            package="nav2_planner",
            executable="planner_server",
            name="planner_server",
            namespace=namespace,
            output="screen",
            parameters=[params_file, {
                "use_sim_time": False,
                # "global_costmap.global_costmap.robot_base_frame": "base_link", # Or 'husky2/base_link'
                # "global_costmap.global_costmap.obstacle_layer.scan.topic": "/husky2/sensors/lidar3d_0/scan",
            }],
            remappings=[("/tf", "/jackal1/tf"), ("/tf_static", "/jackal1/tf_static")],
        ),

        # Controller Server
        Node(
            package="nav2_controller",
            executable="controller_server",
            name="controller_server",
            namespace=namespace,
            output="screen",
            parameters=[params_file, {
                "use_sim_time": False,
                # "local_costmap.local_costmap.robot_base_frame": "base_link",
                # "local_costmap.local_costmap.voxel_layer.scan.topic": "/husky2/sensors/lidar3d_0/scan",
            }],
            remappings=[("/tf", "/jackal1/tf"), 
                        ("/tf_static", "/jackal1/tf_static"),
                        ("odom", "platform/odom/filtered")],
        ),

        # Behavior Tree Navigator
        Node(
            package="nav2_bt_navigator",
            executable="bt_navigator",
            name="bt_navigator",
            namespace=namespace,
            output="screen",
            parameters=[params_file, {"use_sim_time": False}],
            remappings=[("/tf", "/jackal1/tf"), 
                        ("/tf_static", "/jackal1/tf_static"),
                        ("odom", "platform/odom/filtered"),
                        ("scan", "sensors/lidar3d_0/scan")],
        ),

        # Behavior Server
        Node(
            package="nav2_behaviors",
            executable="behavior_server",
            name="behavior_server",
            namespace=namespace,
            output="screen",
            parameters=[params_file, {"use_sim_time": False}],
            remappings=[("/tf", "/jackal1/tf"), 
                        ("/tf_static", "/jackal1/tf_static"),
                        ("odom", "platform/odom/filtered"),
                        ("scan", "sensors/lidar3d_0/scan")],
        ),

        # Lifecycle Manager
        Node(
            package="nav2_lifecycle_manager",
            executable="lifecycle_manager",
            name="lifecycle_manager",
            namespace=namespace,
            output="screen",
            parameters=[{
                "use_sim_time": False,
                "autostart": True,
                "node_names": [
                    "map_server", 
                    "amcl", 
                    "planner_server", 
                    "controller_server", 
                    "bt_navigator",
                    "behavior_server"
                ], 
            }],
        ),
    ])
