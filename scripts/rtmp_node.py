#! /usr/bin/env python

import rospy
import subprocess
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

# import ffmpeg

class ROS2RTMP:
  """
  Subscribes to a ROS desired image topic and pushes it to RTMP server
  """
  def __init__(self):
    self._rtmp_url=rospy.get_param('~rtmp_url', 'rtmp://127.0.0.1:1935/live/webcam') 

    # Desired image height
    self._height = rospy.get_param('~height', 480)
    # Desired image width
    self._width = rospy.get_param('~width', 640)
    # Desired frequency of streaming to rtmp server
    self._fps = rospy.get_param('~fps', 30)

    # True: convert image to gray scale
    self._toGray = rospy.get_param('~toGray', False)

    if self._toGray:
      pix_fmt="gray"
    else:
      pix_fmt="bgr24"

    self._cvBridge = CvBridge()

    self._command = ["ffmpeg",
            "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-pix_fmt", pix_fmt,
            "-s", "{}x{}".format(self._width, self._height),
            "-r", str(self._fps),
            "-i", "-",
            "-c:v", "libx264",
            '-pix_fmt', 'yuv420p',
            "-preset", "ultrafast",
            "-f", "flv",
            "-tune", "zerolatency",
            self._rtmp_url]

    self._rosRate = rospy.Rate(self._fps)

    # ROS image subscriber
    rospy.Subscriber("camera/image_raw", Image, self.imgCallback)

    # CV Image
    self._cvFrame = None
            
    # using subprocess and pipe to fetch frame data
    try:
      self._p = subprocess.Popen(self._command, stdin=subprocess.PIPE)
    except Exception as e:
      rospy.logerr("Could not create ffmpeg pipeline. Error %s", e)
      exit()

  def imgCallback(self, msg):
    """ROS image callback
    """
    try:
      cv_image = self._cvBridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError as e:
      rospy.logerr_throttle(1, "Error in converting ROS image to CV.  Error : %s", e)
      return

    (rows,cols,channels) = cv_image.shape

    # Resize the image, if needed
    if rows != self._height or cols != self._width:
      cv_image = cv2.resize(cv_image, (self._width, self._height), interpolation = cv2.INTER_AREA)
    
    # Convert to gray image, if needed
    if self._toGray:
      cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    self._cvFrame = cv_image
  
  def loop(self):
    """Main loop. Runs at the desired self._fps
    """
    while not rospy.is_shutdown():
      # write to pipe
      if self._cvFrame is not None:
        try:
          self._p.stdin.write(self._cvFrame.tobytes())
        except Exception as e:
          rospy.logwarn_throttle(1, "Error in writing frame to RMTP server. Error: %s", e)
          
      self._rosRate.sleep()

if __name__ == "__main__":
  rospy.init_node("ros2rtmp_node", anonymous=True)

  obj = ROS2RTMP()
  obj.loop()