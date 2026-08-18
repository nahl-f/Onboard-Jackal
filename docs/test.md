# Onboard-Jackal Navigation and Mapping

This repository contains the onboard launch configurations and maps required to run SLAM and Nav2 on the Clearpath Jackal.

## Repository Structure
```text
Onboard-Jackal/
├── maps/                   # Saved maps generated via SLAM
└── real_jackal/
    ├── config/             # Parameter files for navigation and localization
    └── launch/             # Launch files for SLAM, Nav2, and sensors
```

---

## 1. Initial Setup

### Hardware Connection
1. Turn on the Jackal.
2. Connect an Ethernet cable from the Jackal to your laptop.

### Network Configuration (Laptop)
1. Navigate to your laptop's **Settings > Network > Wired**.
2. Click the **+** (plus) icon at the top to create a new profile.
3. Go to the **IPv4** tab and select **Manual**.
4. Populate the fields as follows:

| Setting | Value |
| :--- | :--- |
| **Address** | `192.168.131.101` |
| **Netmask** | `255.255.255.0` |

*(Insert your screenshot here)*
![IPv4 Configuration Screenshot](docs/images/ipv4_setup.png)

### Establishing Connection
Open a terminal on your laptop and verify the connection:
```bash
ping 192.168.131.1
```
If successful, SSH into the Jackal:
```bash
ssh administrator@192.168.131.1
```

### Workspace Setup (Onboard Jackal)
Once connected via SSH, clone and build the repository:
```bash
git clone https://github.com/nahl-f/Onboard-Jackal
cd Onboard-Jackal
colcon build
source install/setup.bash
```

> **Note:** Ensure you have the Docker container set up on your laptop before proceeding. Please refer to the [Offboard Repository Instructions](link-to-other-repo) for laptop environment setup.

---

## 2. Mapping

### Step A: Launch SLAM (Onboard Jackal)
Start the SLAM stack to begin generating a map.
```bash
cd ~/Onboard-Jackal
source install/setup.bash
ros2 launch jackal_nav slam.launch.py
```

### Step B: Visualize Map (Laptop / Docker)
Open a terminal **inside the laptop's Docker container** to view the mapping process:
```bash
cd /workspaces/ros_ws/scripts
source ros_ethernet.env
ros2 launch clearpath_viz view_navigation.launch.py namespace:=jackal1
```

### Step C: Save the Map (Laptop)
Once mapping is complete, open a **new terminal** on the laptop (inside the Docker container) to save the map:
```bash
ros2 run nav2_map_server map_saver_cli -f <map_name> --ros-args -r map:=/jackal1/map
```
> **Next Step:** Follow the steps in the [Offboard Repository](link-to-other-repo) for preparing the map for the navigation system.

---

## 3. Navigation

### Step A: Launch Navigation Stack (Onboard Jackal)
Open **two SSH terminals** into the Jackal.

**Terminal 1:** Launch localization with your saved map.
```bash
cd ~/Onboard-Jackal
source install/setup.bash
ros2 launch jackal_nav localisation.launch.py map:=<path_to_map>
```

**Terminal 2:** Launch Nav2.
```bash
cd ~/Onboard-Jackal
source install/setup.bash
ros2 launch jackal_nav nav2.launch.py 
```

### Step B: Visualize Navigation (Laptop / Docker)
Open a terminal **inside the laptop's Docker container**:
```bash
cd /workspaces/ros_ws/scripts
source ros_ethernet.env
ros2 launch clearpath_viz view_navigation.launch.py namespace:=jackal1
```
