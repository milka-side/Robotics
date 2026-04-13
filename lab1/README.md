# Lab 1: Building Your Robot in Gazebo


## Learning Goals

1. Understand SDF format and structure
2. Create a four-wheeled mobile robot
3. Add a differential drive controller
4. Integrate a LiDAR sensor for environment sensing

---

## Tutorial Workflow

Follow these three official Gazebo tutorials in sequence:

### Part 1: Building Your Own Robot
**Tutorial:** https://gazebosim.org/docs/harmonic/building_robot/

**What you'll do:**
1. Follow the tutorial to understand the structure
2. Create `lab1/worlds/robot.sdf` (your final file)
3. Build robot model with **4 wheels** instead of 2 wheels + caster:
   - Chassis (box link)
   - Left front wheel (cylinder, revolute joint)
   - Right front wheel (cylinder, revolute joint)
   - Left rear wheel (cylinder, revolute joint)
   - Right rear wheel (cylinder, revolute joint)
4. Set inertial properties for all links
5. Test in Gazebo

**Important:** The tutorial shows a 3-wheeled robot (2 wheels + caster). Your task is to modify it to have **4 wheels** - 2 on each side.

**Key SDF concepts:**
- `<world>`, `<model>`, `<link>`, `<joint>`
- `<visual>`, `<collision>`, `<inertial>`
- `<pose>` and reference frames
- Joint types: `revolute`

**Launch command:**
```bash
gz sim /opt/ws/src/code/lab1/worlds/robot.sdf
```

---

### Part 2: Moving the Robot
**Tutorial:** https://gazebosim.org/docs/harmonic/moving_robot/

**What you'll do:**
1. Add differential drive plugin to your robot
2. Configure **4-wheel** differential drive
3. Test robot movement with keyboard commands

**Edit your `lab1/worlds/robot.sdf`:**

Add inside `<model>` tag:
```xml
<plugin filename="gz-sim-diff-drive-system"
        name="gz::sim::systems::DiffDrive">
    <!-- For 4-wheel drive, list both front and rear joints -->
    <left_joint>left_front_wheel_joint</left_joint>
    <left_joint>left_rear_wheel_joint</left_joint>
    <right_joint>right_front_wheel_joint</right_joint>
    <right_joint>right_rear_wheel_joint</right_joint>
    <wheel_separation>1.2</wheel_separation>
    <wheel_radius>0.4</wheel_radius>
    <odom_publish_frequency>1</odom_publish_frequency>
    <topic>cmd_vel</topic>
</plugin>
```

**Note:** Adjust joint names to match your actual wheel joint names!

**Test movement:**
- Launch Gazebo: `gz sim /opt/ws/src/code/lab1/worlds/robot.sdf`
- Use arrow keys or publish to `/cmd_vel` topic
- All 4 wheels should rotate together

---

### Part 3: Adding Sensors (LiDAR)
**Tutorial:** https://gazebosim.org/docs/harmonic/sensors/

**What you'll do:**
1. Add a LiDAR sensor link to your robot
2. Configure sensor properties (range, resolution)
3. Visualize LiDAR data in Gazebo

**Add LiDAR to your robot:**

Add new link inside `<model>`:
```xml
<link name='lidar_link'>
    <pose relative_to='chassis'>0.8 0 0.5 0 0 0</pose>
    <inertial>
        <mass>0.1</mass>
        <inertia>
            <ixx>0.000166667</ixx>
            <iyy>0.000166667</iyy>
            <izz>0.000166667</izz>
        </inertia>
    </inertial>
    <visual name='visual'>
        <geometry>
            <cylinder>
                <radius>0.05</radius>
                <length>0.1</length>
            </cylinder>
        </geometry>
    </visual>
    <sensor name='gpu_lidar' type='gpu_lidar'>
        <topic>lidar</topic>
        <update_rate>10</update_rate>
        <lidar>
            <scan>
                <horizontal>
                    <samples>640</samples>
                    <resolution>1</resolution>
                    <min_angle>-1.396263</min_angle>
                    <max_angle>1.396263</max_angle>
                </horizontal>
            </scan>
            <range>
                <min>0.08</min>
                <max>10.0</max>
            </range>
        </lidar>
        <visualize>true</visualize>
    </sensor>
</link>

<joint name='lidar_joint' type='fixed'>
    <parent>chassis</parent>
    <child>lidar_link</child>
</joint>
```

**Also add sensors system plugin to `<world>`:**
```xml
<plugin filename="gz-sim-sensors-system"
        name="gz::sim::systems::Sensors">
    <render_engine>ogre2</render_engine>
</plugin>
```

---

## Lab Requirements

By the end of this lab, your `robot.sdf` file must include:

1. **4-Wheel Mobile Robot**
   - Chassis (main body)
   - 4 wheels (2 left, 2 right) with revolute joints
   - Proper inertial properties for all links

2. **Differential Drive Plugin**
   - Configured for 4-wheel drive
   - All 4 wheel joints properly linked
   - Responds to `/cmd_vel` commands

3. **LiDAR Sensor**
   - Mounted on the robot
   - Publishing to `/lidar` topic
   - Visualize enabled

4. **Test Objects**
   - At least 3 obstacles in the world
   - Different shapes (boxes, cylinders, etc.)

**Note:** The Gazebo tutorials show a 3-wheeled robot (2 wheels + caster). You must modify it to have **4 wheels**.

---
![Robot Demo](../docs/reference_demo.gif)

## Testing Your Robot

```bash
# Enter Docker container
./scripts/cmd bash

# Launch Gazebo with your robot world
gz sim /opt/ws/src/code/lab1/worlds/robot.sdf

# In another terminal, list topics
gz topic -l

# Look at the lidar messages on the /lidar topic, specifically the ranges data
gz topic -e -t /lidar

# Send movement command (example)
gz topic -t "/cmd_vel" -m gz.msgs.Twist -p "linear: {x: 0.5}, angular: {z: 0.2}"
```

## Resources

- [Building Your Own Robot](https://gazebosim.org/docs/harmonic/building_robot/)
- [Moving the Robot](https://gazebosim.org/docs/harmonic/moving_robot/)
- [Sensors Tutorial](https://gazebosim.org/docs/harmonic/sensors/)
- [SDF Format](http://sdformat.org/)
- [Gazebo Harmonic API](https://gazebosim.org/api/sim/8/)

---
