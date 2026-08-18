## Jackal Setup Guide 
This repository contains the launch files required to run nav2 onboard the RoboHub Jackal. These launch and configuration files have only been tested with **ROS2 Humble**

## Repository Structure
```text
Onboard-Jackal/
├── maps/                   # To store maps
└── real_jackal/
    ├── config/             # Config files for navigation and localization
    └── launch/             # Launch files for SLAM & Nav2
```
## Initial Setup
### Ethernet Setup
- On your laptop, **Settings > Network > Wired**
- Click the plus (**+**) icon at the top to create a new profile
- Go to the **IPv4** tab and click **Manual** 
- Fill in the fields as shown below:
  - Addresses: 192.168.131.101
  - Netmask: 255.255.255.0
 - Click **Add** and choose that profile
### Connecting to the Jackal
- Turn the Jackal on
- Connect an ethernet cable from the Jackal to your Laptop
  - Ensure the profile is chosen in your wired settings
- Open a terminal and test the connection
```
ping 192.168.131.1
```
- If successful, ssh into the Jackal
```
ssh administrator@192.168.131.1
```
### Workspace Setup
#### Onboard Computer (Jackal)
```
git clone https://github.com/nahl-f/Onboard-Jackal
cd ~/Onboard-Jackal
colcon build
source install/setup.bash
```
#### Offboard Computer (Laptop)

Ensure you have the [Jackal Docker Container](https://github.com/nahl-f/Jackal-Person-Nav) setup on your laptop.
In the docker container:
```
cd /workspaces/ros_ws/scripts
source ros_ethernet.env
ros2 topic list
ros2 node list
```
## Mapping
### Onboard Computer (Jackal)

Launch SLAM to begin generating the map:
```
cd ~/Onboard-Jackal
source install/setup.bash
ros2 launch jackal_nav slam.launch.py
```
### Offboard Computer (Laptop)

- **Terminal 1**
  
Open a terminal inside the laptop's docker container to view the mapping process:
```text
cd /workspaces/ros_ws/scripts
source ros_ethernet.env
ros2 launch clearpath_viz view_navigation.launch.py namespace:=jackal1
```
- **Terminal 2**  

After mapping is complete, run the following command to save a **map.pgm** and **map.yaml** in your current directory.
```text
cd /workspaces/ros_ws/scripts
source ros_ethernet.env
cd /workspaces/ros_ws/src/project/config/maps
ros2 run nav2_map_server map_saver_cli -f <map_name> --ros-args -r map:=/jackal1/map
```
## Navigation
### Onboard Computer (Jackal)

- **Terminal 1**

Start localisation against the map of the environment.
```text
cd /workspaces/ros_ws/scripts
source ros_ethernet.env
ros2 launch clearpath_viz localisation.launch.py map:=<path to map>
```
- **Terminal 2**

While localisation is running, start the complete nav2 stack
```text
cd /workspaces/ros_ws/scripts
source ros_ethernet.env
cd /workspaces/ros_ws/src/project/config/maps
ros2 run nav2_map_server map_saver_cli -f <map_name> --ros-args -r map:=/jackal1/map
```
