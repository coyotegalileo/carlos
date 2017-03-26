#!/usr/bin/env python

import rospy
import math
import random
import param
import resample
import message
import maps
import tf
import time
from motion import motion
from perception import perception
from state import PoseState
from geometry_msgs.msg import PoseArray
from geometry_msgs.msg import PoseWithCovariance
from visualization_msgs.msg import MarkerArray
from nav_msgs.msg import Odometry
from nav_msgs.msg import OccupancyGrid
from std_msgs.msg import Float32MultiArray



# mcl algorithm
def mcl(state, u, z):

    # Variavel de Normalizacao    
    wsum = 0.0
    # Variaveis de medida de confianca
    wavg = 0.0
    wfast = param.wfast
    wslow = param.wslow

    # transforma u nas varias componentes separadas
    u_x = [u[0] ,u[3]]
    u_y = [u[1] ,u[4]]
    u_t = [u[2] ,u[5]]
    
    # em cada ciclo variavel reiniciada
    x = []
    y = []
    t = []
    w = []
      
    # Prediction e Update
    for i in range(param.M):        

        # funcao com o motion model
        xaux , yaux, taux = motion(u_x, u_y, u_t, state.x[i], state.y[i], state.t[i])

        # Inicia Waux        
        waux = 1.0 
        waux = waux * maps.mapa(xaux, yaux)        
        # funcao com o perception model
        waux = perception(z, [xaux, yaux, taux]) * waux
                        
        # adicionar as novas particulas
        x[len(x):] = [xaux]
        y[len(y):] = [yaux]
        t[len(t):] = [taux]
        w[len(w):] = [waux * state.w[i]] 
        wsum = wsum + waux * state.w[i]
        wavg = wavg + waux * state.w[i] / param.M
   
    # normalizacao dos pesos  
    for i in range(param.M):
        if wsum > 0:
            w[i] = float (w[i]) / wsum        

    #atribuicao ao estado dos novos valores
    state.x = x
    state.y = y
    state.t = t
    state.w = w 

    # Determinacao de confianca das particulas
    wslow = wslow + param.alphaslow * (wavg - wslow)
    wfast = wfast + param.alphafast * (wavg - wfast)

    # Probabilidade de falha ou kidnap
    kidnap_prob = max([0.0 , 1 - wfast / wslow ])

    # Calculo da pose media
    mean_pose = state.rosbustmean()

    print kidnap_prob , wfast, wslow, wavg   

    # Resampling             
    neff = resample.eff_particles(state.w)
    # Verificar numero efectivo de particulas
    if neff < 1 * param.M / 3:                 
        state = resample.kidnap_resample(state, kidnap_prob, z )                

    # Guarda wfast
    param.wfast = wfast
    param.wslow = wslow
    
    return state, mean_pose  


# Retirar dados da subscricao de odometria
def callback(data):   
    param.odometry = data    


# Tratamento dos dados odometricos
def getOdom(odometry):   
    # Posicao
    position = odometry.pose.pose.position
    # Orientacao    
    q = odometry.pose.pose.orientation
    euler = tf.transformations.euler_from_quaternion([q.x ,q.y ,q.z ,q.w], 'sxyz')   
    theta = euler[2] - math.floor(euler[2]/(2*math.pi))*2*math.pi   
   
    return position.x, position.y, theta


# Rececao de observacoes
def incomingMeasure(data):
    param.measure = data.data
    
# Obter frame actual
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

# Rececao de observacoes
def incomingMap(data):

    param.mapa = data
    param.mapreceive = True   


# MAIN
if __name__ == '__main__':
    try:
        # inicializacao de publishers        
        pub_pose = rospy.Publisher('/mcl/particles', PoseArray, queue_size=param.M)
        pub_estimate = rospy.Publisher('/mcl/estimate', PoseArray, queue_size=5)       
        pub_landmarks = rospy.Publisher('/mcl/landmark/markers', MarkerArray, queue_size=len(param.feat))

        # inicializacao de subscribers
        rospy.Subscriber('/RosAria/pose', Odometry, callback)
        rospy.Subscriber('/processing/measurements', Float32MultiArray, incomingMeasure)
        rospy.Subscriber('/map', OccupancyGrid, incomingMap)

        # inicializacao do node
        rospy.init_node('mcl', anonymous=True)

        # definicao da estrutura da mensagem
        msg = message.message_pose_array(param.M)
        robustmeanmsg = message.message_pose_array(1)
        landmark = message.message_landmarks()

        #inicializacao do odometry
        u = [0] * 6
        u[3], u[4], u[5] = getOdom(param.odometry) 
        
        #inicializacao de observacoes
        z = []        

        # define and broadcast frames
        br = tf.TransformBroadcaster()
        br.sendTransform((0, 0, 0),
            tf.transformations.quaternion_from_euler(0, 0, 0),
            rospy.Time.now(),'/mcl/particles',"world") 
        br.sendTransform((0, 0, 0),
            tf.transformations.quaternion_from_euler(0, 0, 0),
            rospy.Time.now(),'/mcl/estimate',"world")   
        br.sendTransform((0, 0, 0),
            tf.transformations.quaternion_from_euler(0, 0, 0),
            rospy.Time.now(),'odom',"world")  
        br1 = tf.TransformBroadcaster()
        br1.sendTransform((0, 0, 0),
            tf.transformations.quaternion_from_euler(0, 0, 0),
            rospy.Time.now(),"/map","world")  

        # inicializacao do estado
        state = PoseState(param.M)   

        # publica primeira mensagem
        for i in range(param.M):
             # Obter quaterniao
             q = tf.transformations.quaternion_from_euler(0, 0, state.t[i])
             # Transformar estado em mensagem      
             msg.poses[i].position.x = state.x[i]
             msg.poses[i].position.y = state.y[i]
             msg.poses[i].orientation.x = q[0]
             msg.poses[i].orientation.y = q[1]
             msg.poses[i].orientation.z = q[2]
             msg.poses[i].orientation.w = q[3]
        pub_pose.publish(msg)
        
        # Frequencia max do algoritmo
        rate = rospy.Rate(10) 

        while not rospy.is_shutdown():  

            # define and broadcast frames
            br = tf.TransformBroadcaster()
            br.sendTransform((0, 0, 0),
                tf.transformations.quaternion_from_euler(0, 0, 0),
                rospy.Time.now(),'/mcl/particles',"world") 
            br.sendTransform((0, 0, 0),
                tf.transformations.quaternion_from_euler(0, 0, 0),
                rospy.Time.now(),'/mcl/estimate',"world")    
            br1 = tf.TransformBroadcaster()
            br1.sendTransform((0, 0, 0),
                tf.transformations.quaternion_from_euler(0, 0, 0),
                rospy.Time.now(),"map","world")          

               
            # Odometria
            u[0], u[1], u[2] = u[3], u[4], u[5]
            u[3], u[4], u[5] = getOdom(param.odometry) 
 
            # Observacoes
            z = getMeasure()

            # Sem variacao de odometria nao ha accao
            if u[3]-u[0]==0 and u[4]-u[1]==0 and u[5]-u[2]==0:                
                continue    
            else:
                # Augmented MCL
                state, mean_pose = mcl(state, u, z) 
                                           
            # Escreve estimativa como mensagem
            # Obter quaterniao de euler
            q = tf.transformations.quaternion_from_euler(0, 0, mean_pose[2])
            # Transformar estado em mensagem  
            robustmeanmsg.poses[0].position.x = mean_pose[0]
            robustmeanmsg.poses[0].position.y = mean_pose[1]
            robustmeanmsg.poses[0].position.z = 0.02
            robustmeanmsg.poses[0].orientation.x = q[0]
            robustmeanmsg.poses[0].orientation.y = q[1]
            robustmeanmsg.poses[0].orientation.z = q[2]
            robustmeanmsg.poses[0].orientation.w = q[3]
            
            # Escreve todas as particulas como mensagem
            for i in range(param.M):
                 # Obter quaterniao
                 q = tf.transformations.quaternion_from_euler(0, 0, state.t[i])
                 # Transformar estado em mensagem      
                 msg.poses[i].position.x = state.x[i]
                 msg.poses[i].position.y = state.y[i]
                 msg.poses[i].orientation.x = q[0]
                 msg.poses[i].orientation.y = q[1]
                 msg.poses[i].orientation.z = q[2]
                 msg.poses[i].orientation.w = q[3]                 
            
            # publica mensagem
            pub_estimate.publish(robustmeanmsg)
            # publica mensagem
            pub_pose.publish(msg)
            # visuliza landmark publica
            pub_landmarks.publish(landmark)                         
                    
            rate.sleep()  
        
        
    except rospy.ROSInterruptException:
	     pass

