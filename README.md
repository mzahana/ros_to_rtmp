# rtmp_to_ros
ROS package that can be used to stream a ROS image topic to RTMP server.

# Installation
Tested with ROS Melodic on Ubuntu 18

Install dependencies
```bash
 sudo apt install ffmpeg -y
 pip install ffmpeg-python==0.1.17
 sudo apt install ros-melodic-cvbridge -y
```

# Run
```bash
roslaunch ros_to_rtmp rtmp_node.launch rtmp_url:=<rtmp_server_url> img_topic:=<image/topic>
```
Make sure that the `rtmp_url` and `img_topic` arguments is set properly.

To control the stream, check the default parameters in the launch file rtmp_node.launch to control the stream
