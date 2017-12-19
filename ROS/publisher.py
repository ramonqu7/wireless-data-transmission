from openni2_device_init import VisionSensor
import rospy
from std_msgs.msg import Int16MultiArray
import mraa
import time
import zlib
import rospy

class RgbdPublisher():
    def __init__(self):
        self.device = VisionSensor()
        self.device.createDepth() # default 640*480*30fps
        self.RosInit()

    def RosInit(self):
        self.node = rospy.Publisher('CameraTest')
        rospy.init_node("Joule", anonymous=False)

    def publishFrame(self):
        while not rospy.is_shutdown():
            data = self.device.getDepth()
            self.node.publish(data)


if __name__ == '__main__':
    try:
        rgbd = RgbdPublisher()
    except rospy.ROSInterruptException:
        print("ROS Interrupt")