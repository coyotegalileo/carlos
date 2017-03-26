#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseArray
from geometry_msgs.msg import Pose

current = PoseArray()
currentlaser = Pose()

read = 0
readlaser = 0
