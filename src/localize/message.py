#!/usr/bin/env python

import param
import rospy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayDimension
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import PoseArray
from geometry_msgs.msg import Pose
from visualization_msgs.msg import MarkerArray
from visualization_msgs.msg import Marker

####Mensagens
# Pose unica
def message_pose():
    msg = PoseStamped()
    msg.pose.position.z = 0
    msg.header.frame_id = 'world'

    return msg


# Para visualizar poses
def message_pose_array(n):

    msg = PoseArray()
    for i in range(n):
        msg.poses.append(Pose())
        msg.poses[i].position.z = 0
    msg.header.frame_id = 'world'

    return msg

# Para visualizar landmarks
def message_landmarks():
    msg = MarkerArray()

    for i in range(len(param.feat)):
        msg.markers.append(Marker())
        msg.markers[i].id = i
        if param.feat[i][2] == 1:
            msg.markers[i].ns = "lm"
            msg.markers[i].action = Marker.ADD
            msg.markers[i].type = Marker.CYLINDER
            msg.markers[i].pose.position.x = param.feat[i][0]
            msg.markers[i].pose.position.y = param.feat[i][1]
            msg.markers[i].pose.position.z = 0.15
            msg.markers[i].lifetime = rospy.Duration(10)
            msg.markers[i].color.r = 1.0 * 255/255
            msg.markers[i].color.g = 192.0 /255.0 
            msg.markers[i].color.b = 203.0/255.0
            msg.markers[i].color.a = 1.0
            msg.markers[i].frame_locked = True
            msg.markers[i].header.frame_id = 'world'
        
        if param.feat[i][2] == 2:
            msg.markers[i].ns = "lm"
            msg.markers[i].action = Marker.ADD
            msg.markers[i].type = Marker.CYLINDER
            msg.markers[i].pose.position.x = param.feat[i][0]
            msg.markers[i].pose.position.y = param.feat[i][1]
            msg.markers[i].pose.position.z = 0.15
            msg.markers[i].lifetime = rospy.Duration(10)
            msg.markers[i].color.r = 255.0/255.0
            msg.markers[i].color.g = 192.0 /255.0 
            msg.markers[i].color.b = 203.0/255.0
            msg.markers[i].color.a = 1.0
            msg.markers[i].frame_locked = True
            msg.markers[i].header.frame_id = 'world'

        if param.feat[i][2] == 3:
            msg.markers[i].ns = "lm"
            msg.markers[i].action = Marker.ADD
            msg.markers[i].type = Marker.CYLINDER
            msg.markers[i].pose.position.x = param.feat[i][0]
            msg.markers[i].pose.position.y = param.feat[i][1]
            msg.markers[i].pose.position.z = 0.15
            msg.markers[i].lifetime = rospy.Duration(10)
            msg.markers[i].color.r = 255.0/255.0
            msg.markers[i].color.g = 255.0 /255.0 
            msg.markers[i].color.b = 0.0/255.0
            msg.markers[i].color.a = 1.0
            msg.markers[i].frame_locked = True
            msg.markers[i].header.frame_id = 'world'

        if param.feat[i][2] == 4:
            msg.markers[i].ns = "lm"
            msg.markers[i].action = Marker.ADD
            msg.markers[i].type = Marker.CYLINDER
            msg.markers[i].pose.position.x = param.feat[i][0]
            msg.markers[i].pose.position.y = param.feat[i][1]
            msg.markers[i].pose.position.z = 0.15
            msg.markers[i].lifetime = rospy.Duration(10)
            msg.markers[i].color.r = 0
            msg.markers[i].color.g = 0 
            msg.markers[i].color.b = 255.0/255.0
            msg.markers[i].color.a = 1.0
            msg.markers[i].frame_locked = True
            msg.markers[i].header.frame_id = 'world'
        
        msg.markers[i].scale.x = 0.3
        msg.markers[i].scale.y = 0.3
        msg.markers[i].scale.z = 0.3
   
    for j in range(len(param.feat)):
        msg.markers.append(Marker())
        i = j + 4
        msg.markers[i].id = i 
        if param.feat[j][2] == 1:
            msg.markers[i].ns = "lm"
            msg.markers[i].action = Marker.ADD
            msg.markers[i].type = Marker.CYLINDER
            msg.markers[i].pose.position.x = param.feat[j][0]
            msg.markers[i].pose.position.y = param.feat[j][1]
            msg.markers[i].pose.position.z = 0.15 + 0.3
            msg.markers[i].lifetime = rospy.Duration(10)
            msg.markers[i].color.r = 255.0/255.0
            msg.markers[i].color.g = 255.0 /255.0 
            msg.markers[i].color.b = 0.0/255.0
            msg.markers[i].color.a = 1.0
            msg.markers[i].frame_locked = True
            msg.markers[i].header.frame_id = 'world'
        
        if param.feat[j][2] == 2:
            msg.markers[i].ns = "lm"
            msg.markers[i].action = Marker.ADD
            msg.markers[i].type = Marker.CYLINDER
            msg.markers[i].pose.position.x = param.feat[j][0]
            msg.markers[i].pose.position.y = param.feat[j][1]
            msg.markers[i].pose.position.z = 0.15 + 0.3
            msg.markers[i].lifetime = rospy.Duration(10)
            msg.markers[i].color.r = 0
            msg.markers[i].color.g = 0 
            msg.markers[i].color.b = 255.0/255.0
            msg.markers[i].color.a = 1.0
            msg.markers[i].frame_locked = True
            msg.markers[i].header.frame_id = 'world'

        if param.feat[j][2] == 3:
            msg.markers[i].ns = "lm"
            msg.markers[i].action = Marker.ADD
            msg.markers[i].type = Marker.CYLINDER
            msg.markers[i].pose.position.x = param.feat[j][0]
            msg.markers[i].pose.position.y = param.feat[j][1]
            msg.markers[i].pose.position.z = 0.15 + 0.3
            msg.markers[i].lifetime = rospy.Duration(10)
            msg.markers[i].color.r = 1.0 * 255/255
            msg.markers[i].color.g = 192.0 /255.0 
            msg.markers[i].color.b = 203.0/255.0            
            msg.markers[i].color.a = 1.0
            msg.markers[i].frame_locked = True
            msg.markers[i].header.frame_id = 'world'

        if param.feat[j][2] == 4:
            msg.markers[i].ns = "lm"
            msg.markers[i].action = Marker.ADD
            msg.markers[i].type = Marker.CYLINDER
            msg.markers[i].pose.position.x = param.feat[j][0]
            msg.markers[i].pose.position.y = param.feat[j][1]
            msg.markers[i].pose.position.z = 0.15 + 0.3
            msg.markers[i].lifetime = rospy.Duration(10)
            msg.markers[i].color.r = 1.0 * 255 / 255
            msg.markers[i].color.g = 192.0 / 255.0 
            msg.markers[i].color.b = 203.0 / 255.0            
            msg.markers[i].color.a = 1.0
            msg.markers[i].frame_locked = True
            msg.markers[i].header.frame_id = 'world'
   
        msg.markers[i].scale.x = 0.3
        msg.markers[i].scale.y = 0.3
        msg.markers[i].scale.z = 0.3

    for j in range(len(param.feat)):
        msg.markers.append(Marker())
        i = j + 4 * 2
        msg.markers[i].id = i
        if param.feat[j][2] == 1:
            msg.markers[i].ns = "lm"
            msg.markers[i].action = Marker.ADD
            msg.markers[i].type = Marker.CYLINDER
            msg.markers[i].pose.position.x = param.feat[j][0]
            msg.markers[i].pose.position.y = param.feat[j][1]
            msg.markers[i].pose.position.z = 0.15 + 0.3 *2
            msg.markers[i].lifetime = rospy.Duration(10)
            msg.markers[i].color.r = 255.0/255.0
            msg.markers[i].color.g = 255.0 /255.0 
            msg.markers[i].color.b = 255.0/255.0
            msg.markers[i].color.a = 1.0
            msg.markers[i].frame_locked = True
            msg.markers[i].header.frame_id = 'world'
        
        if param.feat[j][2] == 2:
            msg.markers[i].ns = "lm"
            msg.markers[i].action = Marker.ADD
            msg.markers[i].type = Marker.CYLINDER
            msg.markers[i].pose.position.x = param.feat[j][0]
            msg.markers[i].pose.position.y = param.feat[j][1]
            msg.markers[i].pose.position.z = 0.15 + 0.3 *2
            msg.markers[i].lifetime = rospy.Duration(10)
            msg.markers[i].color.r = 255.0/255.0
            msg.markers[i].color.g = 255.0 /255.0 
            msg.markers[i].color.b = 255.0/255.0
            msg.markers[i].color.a = 1.0
            msg.markers[i].frame_locked = True
            msg.markers[i].header.frame_id = 'world'

        if param.feat[j][2] == 3:
            msg.markers[i].ns = "lm"
            msg.markers[i].action = Marker.ADD
            msg.markers[i].type = Marker.CYLINDER
            msg.markers[i].pose.position.x = param.feat[j][0]
            msg.markers[i].pose.position.y = param.feat[j][1]
            msg.markers[i].pose.position.z = 0.15 + 0.3 *2
            msg.markers[i].lifetime = rospy.Duration(10)
            msg.markers[i].color.r = 255.0/255.0
            msg.markers[i].color.g = 255.0 /255.0 
            msg.markers[i].color.b = 255.0/255.0          
            msg.markers[i].color.a = 1.0
            msg.markers[i].frame_locked = True
            msg.markers[i].header.frame_id = 'world'

        if param.feat[j][2] == 4:
            msg.markers[i].ns = "lm"
            msg.markers[i].action = Marker.ADD
            msg.markers[i].type = Marker.CYLINDER
            msg.markers[i].pose.position.x = param.feat[j][0]
            msg.markers[i].pose.position.y = param.feat[j][1]
            msg.markers[i].pose.position.z = 0.15 + 0.3 *2
            msg.markers[i].lifetime = rospy.Duration(10)
            msg.markers[i].color.r = 255.0/255.0
            msg.markers[i].color.g = 255.0 /255.0 
            msg.markers[i].color.b = 255.0/255.0          
            msg.markers[i].color.a = 1.0
            msg.markers[i].frame_locked = True
            msg.markers[i].header.frame_id = 'world'
   
        msg.markers[i].scale.x = 0.3
        msg.markers[i].scale.y = 0.3
        msg.markers[i].scale.z = 0.3
    

    return msg
