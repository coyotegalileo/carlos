#!/usr/bin/env python

import rospy
import math
import random
import param
from perception import perception
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32MultiArray

def incomingMeasure(data):
  param.measure = data.data
    
def getMeasure():
    newmeasure = param.measure
    
    formated = []

    # formatacao    
    for i in range(len(newmeasure)/3):
        zData = []
        zData.append(newmeasure[1 + i * 3]) #r
        zData.append(newmeasure[2 + i * 3]) #b
        zData.append(newmeasure[0 + i * 3]) #id
        formated.append(zData)

    return formated


# PROGRAMA COMECA AQUI
if __name__ == '__main__':
    try:       
        # inicializacao do subscriber
        #rospy.Subscriber('/RosAria/pose', Odometry, callback)
        rospy.Subscriber('/processing/measurements', Float32MultiArray, incomingMeasure)

        # inicializacao do node
        rospy.init_node('mcl', anonymous=True)


        # Grid
        pose = []
        # Grid Attribution
        side = 100
        xlim = 10.0
        ylim = 10.0
        thetaSize = 20
        th = 0.0
        for k in range(thetaSize):
            th = th + 2*math.pi/thetaSize
            for i in range(side):
                for j in range(side):
                    pose.append([i*2.0*xlim/side-xlim,j*2.0*ylim/side-ylim,th])

        #print pose        
        rate = rospy.Rate(10)
        
        fich = open('diagnose.dat', 'w+')   
        
        while not rospy.is_shutdown():
            z = getMeasure()
            if z:
                #print "Printing"                 
                #for i in range(len(pose)):
                #    q = perception(z, pose[i])
                #    fich.write('%f %f %f %f  \n' % (pose[i][0],pose[i][1],pose[i][2],q))
                #Para manter frequencia --> debug
                for i in range(len(z)):    
                   fich.write('%d %f %f %f \n' % (i,z[i][0],z[i][1],z[i][2]))     
                rate.sleep()  
        
        
    except rospy.ROSInterruptException:
	     pass
