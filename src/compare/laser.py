#!/usr/bin/env python

import rospy
import math      
import tf     

# MAIN
if __name__ == '__main__':
    try:
        # inicializacao do node
        rospy.init_node('transform', anonymous=True)
        
        rate = rospy.Rate(20) 

        while not rospy.is_shutdown():  

    
            # define and broadcast framesS           
            br1 = tf.TransformBroadcaster()
            br1.sendTransform((0, 0, 0),
                tf.transformations.quaternion_from_euler(0, 0, 0),
                rospy.Time.now(),"/map","world")
            br1.sendTransform((0, 0, 0),
                tf.transformations.quaternion_from_euler(0, 0, 0),
                rospy.Time.now(),"/laser","/odom")         
            br1.sendTransform((0, 0, 0),
                tf.transformations.quaternion_from_euler(0, 0, 0),
                rospy.Time.now(),"/odom","world")                                            
                    
            rate.sleep()          
        
    except rospy.ROSInterruptException:
	     pass

