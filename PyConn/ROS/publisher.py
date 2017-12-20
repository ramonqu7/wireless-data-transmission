from openni2_device_init import VisionSensor
import rospy
from std_msgs.msg import String
import mraa
import time

class RgbdPublisher():
    def __init__(self):
        self.device = VisionSensor()

if __name__ == '__main__':
    rgbd = RgbdPublisher()