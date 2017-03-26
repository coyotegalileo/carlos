#!/usr/bin/env python

import rospy
import extern
import tf
import math
from geometry_msgs.msg import PoseArray
from geometry_msgs.msg import PoseWithCovarianceStamped

# Retirar dados da subscricao de odometria
def callback(data):   
    extern.current = data    
    extern.read = 1

# Tratamento dos dados odometricos
def getPose(newpose):   
      
    x = newpose.poses[0].position.x
    y = newpose.poses[0].position.y
    z = newpose.poses[0].position.z
    
    q = newpose.poses[0].orientation
    euler = tf.transformations.euler_from_quaternion([q.x ,q.y ,q.z ,q.w], 'sxyz')   
    t = euler[2] - math.floor(euler[2]/(2*math.pi))*2*math.pi   

    return [x,y,t]

# Retirar dados da subscricao de odometria
def callbacklaser(data):   
    extern.currentlaser = data.pose.pose    
    extern.readlaser = 1

# Tratamento dos dados odometricos
def getPoselaser(newpose):   
      
    x = newpose.position.x
    y = newpose.position.y
    z = newpose.position.z
    
    q = newpose.orientation
    euler = tf.transformations.euler_from_quaternion([q.x ,q.y ,q.z ,q.w], 'sxyz')   
    t = euler[2] - math.floor(euler[2]/(2*math.pi))*2*math.pi   

    return [x,y,t]

# MAIN
if __name__ == '__main__':
    try:

        # inicializacao de subscribers
        rospy.Subscriber('/mcl/estimate', PoseArray, callback)
#        rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, callbacklaser)
 

        # inicializacao do node
        rospy.init_node('log', anonymous=True)

       
       
 

     
        fich = open('log.dat', 'w+')  
#        fichlaser = open('loglaser.dat', 'w+') 
        # Frequencia max do algoritmo
        rate = rospy.Rate(10)
        i = 0 

        while not rospy.is_shutdown():  
           
            
            if extern.read > 0:# and extern.readlaser > 0:
               print i
               i = i + 1
               pose = getPose(extern.current)
#               poselaser = getPoselaser(extern.currentlaser) 
               fich.write('%d %f %f %f \n' % (i,pose[0],pose[1],pose[2]))
#               fichlaser.write('%d %f %f %f \n' % (i,poselaser[0],poselaser[1],poselaser[2]))
               extern.read = 0
#               extern.readlaser = 0
            rate.sleep()  
        
        
    except rospy.ROSInterruptException:
	     pass
