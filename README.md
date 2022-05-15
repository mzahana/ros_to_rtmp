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

# RTMP Server
You can use the Nginx server that is pre-built in a Docker image as described [here](https://hub.docker.com/r/tiangolo/nginx-rtmp/)

# Run
```bash
roslaunch ros_to_rtmp rtmp_node.launch rtmp_url:=<rtmp_server_url> img_topic:=<image/topic>
```
Make sure that the `rtmp_url` and `img_topic` arguments is set properly.

To control the stream, check the default parameters in the launch file rtmp_node.launch to control the stream

# Visualize the stream
To visualize the stream from the RTMP server, you can use player that can receive rtmp streams such as VLC or `mpv`.

`mpv` is recommended, and you can use the following command as an example (tested with low latency)
```bash
mpv   --msg-color=yes   --msg-module=yes   --keepaspect=yes   --no-correct-pts   --untimed   --vd-lavc-threads=1   --cache=no   --cache-pause=no   --demuxer-lavf-o-add="fflags=+nobuffer+fastseek+flush_packets"   --demuxer-lavf-probe-info=nostreams   --demuxer-lavf-analyzeduration=0.1   --demuxer-max-bytes=500MiB   --demuxer-readahead-secs=0.1     --interpolation=no   --hr-seek-framedrop=no   --video-sync=display-resample   --temporal-dither=yes   --framedrop=decoder+vo     --deband=no   --dither=no     --hwdec=auto-copy   --hwdec-codecs=all     --video-latency-hacks=yes   --profile=low-latency   --linear-downscaling=no   --correct-downscaling=yes   --sigmoid-upscaling=yes   --scale=ewa_hanning   --scale-radius=3.2383154841662362   --cscale=ewa_lanczossoft   --dscale=mitchell     --fs   --osc=no   --osd-duration=450   --border=no   --no-pause   --no-resume-playback   --keep-open=no   --network-timeout=0 --stream-lavf-o=reconnect_streamed=1   rtmp://127.0.0.1/live/webcam
```

The `rtmp://127.0.0.1/live/webcam` should match the stream url in the launch file `rtmp_url`

# TODO
- [ ] Add ROS services to configure the stream. For example, change of resolution, fps, image size, ...
