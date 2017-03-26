#!/usr/bin/env python

import rospy
import cv2
import numpy as np
import vvar
import math


from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


def GetDepth(depth):
    vvar.receiveDeep = 1
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(depth, "32FC1")
    vvar.depthImage = cv_image.copy()

# Extracao de frames
def GetImage(color):    
    bridge = CvBridge()
    vvar.colorImage = bridge.imgmsg_to_cv2(color, "bgr8")
    # Para poder iniciar leitura de ficheiros
    vvar.receive = 1

# Funcoes para o tuner    
def changeBarLH(value):
    vvar.iLowH = value
def changeBarHH(value):
    vvar.iHighH = value
def changeBarLS(value):
    vvar.iLowS = value
def changeBarHS(value):
    vvar.iHighS = value
def changeBarLV(value):
    vvar.iLowV = value
def changeBarHV(value):
    vvar.iHighV = value

# Obtem contornos presentes nas imagens
def getContours(choice, OrImg):
    if choice == 'yellow':
        LowH = 19
        HighH = 32
        LowS = 170 
        HighS = 255
        LowV = 0
        HighV = 255

    if choice == 'blue':
        LowH = 80
        HighH = 112
        LowS = 112 
        HighS = 255
        LowV = 0
        HighV = 255

    if choice == 'pink':
        LowH = 137
        HighH = 175
        LowS = 82 
        HighS = 230
        LowV = 0
        HighV = 255

    if choice == 'white':
        LowH = 0
        HighH = 179
        LowS = 0 
        HighS = 30
        LowV = 0
        HighV = 255

    if choice == 'control':
        LowH = vvar.iLowH
        HighH = vvar.iHighH
        LowS = vvar.iLowS
        HighS = vvar.iHighS
        LowV = vvar.iLowV
        HighV = vvar.iHighV
    
    # Threshold desejado
    lowBnd = np.array([LowH, LowS, LowV])
    HighBnd = np.array([HighH, HighS, HighV])

    # Blur 
    BlurImg = cv2.GaussianBlur(OrImg, (5,5), 0)

    # To HSV
    HSVImg = cv2.cvtColor(BlurImg, cv2.COLOR_BGR2HSV)

    # Threshold
    threshImg = cv2.inRange(HSVImg, lowBnd, HighBnd)

    # Morphological Transformations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    # Morphological Opening
    opening = cv2.morphologyEx(threshImg, cv2.MORPH_OPEN, kernel)
    # Morphological Closing
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)    
    # Contours
    closing, contours, hierarchy = cv2.findContours(closing,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(closing, contours, -1, (180,150,150), cv2.LINE_8)

    # Centers of Mass
    cx = []
    cy = []
    area = []
    lista = []
    for i in range(len(contours)):
        M = cv2.moments(contours[i])
        if M['m00'] != 0 :
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            area = cv2.contourArea(contours[i])
            if area > 75 and cx > 35 and cx < 605:
                lista.append([cx,cy,area])       

    return lista, closing

# Analisa contornos e encontra landmarks
def searchLD(ylw, blu, pnk, imag, target):
    
    targetList = []

    # Para cada Rosa
    for i in range(len(pnk)):
        if pnk[i][2] > 90:
            # Para cada amarelo
            for j in range(len(ylw)):
                if ylw[j][2] > 90:            
                    difX = abs(pnk[i][0] - ylw[j][0])

                    # Verificar se existem contornos amarelos no mesmo eixo
                    if ( difX < 35):
                        difY = (pnk[i][1] - ylw[j][1])               
                        difAr = (pnk[i][2] - ylw[j][2]) / pnk[i][2]  

                        # Verificar diferenca de areas             
                        if(abs(difAr) < 0.60):
                            meanA = (pnk [i][2] + ylw[j][2]) / 2
                            
                            # "Landmark 1 Provavel \n[W]\n[Y]\n[P]\n"
                            if(difY < 1 * meanA**0.5 * vvar.scale and difY > 0):                                                   
                                cv2.circle(target,(ylw[j][0],ylw[j][1]), 15, (0,0,255), -1)
                                targetList.append(1)
                                targetList.append(ylw[j][0])
                                targetList.append(ylw[j][1])
                            # "Landmark 3 Provavel \n[W]\n[P]\n[Y]\n"
                            if(difY > -1 * meanA**0.5 * vvar.scale and difY < 0):                        
                                cv2.circle(target,(pnk[i][0],pnk[i][1]), 15, (255,255,0), -1)
                                targetList.append(3)
                                targetList.append(pnk[i][0])
                                targetList.append(pnk[i][1])
    
            # Para cada azul
            for j in range(len(blu)):
                if blu[j][2] > 90:               
                    difX = abs(pnk[i][0] - blu[j][0])
                    # Verificar se existem contornos azuis no mesmo eixo
                    if ( difX < 35):
                        difY = (pnk[i][1] - blu[j][1])              
                        difAr = (pnk[i][2] - blu[j][2]) / pnk[i][2]

                        # Verificar diferenca de areas               
                        if(abs(difAr) < 0.50): 
                            meanA = (pnk [i][2] + blu[j][2]) / 2

                            # "Landmark 2 Provavel [W][B][P]"
                            if(difY < 1 * meanA**0.5 * vvar.scale and difY > 0):                     
                                cv2.circle(target,(blu[j][0],blu[j][1]), 15, (0,255,0), -1)
                                targetList.append(2)
                                targetList.append(blu[j][0])
                                targetList.append(blu[j][1]) 
                            # "Landmark 4 Provavel [W][P][B]" 
                            if(difY > -1 * meanA**0.5 * vvar.scale  and difY < 0):                        
                                cv2.circle(target,(pnk[i][0],pnk[i][1]), 15, (255,0,0), -1)
                                targetList.append(4)
                                targetList.append(pnk[i][0])
                                targetList.append(pnk[i][1])                                    
                           
    return target, targetList

def measurementDetermine(ldm, deepframe, msg):
    
    d = []    
    msg.data = []

    for i in range(len(ldm)/3):
        #mean around a 10x10 square
        rng = 0
        count = 0
        for j in range(10):
            for k in range(10):
                if not math.isnan(deepframe[ldm[2 + 3 * i] - 5 + j,ldm[1 + 3 * i]- 5 + k]):
                  rng = rng + deepframe[ldm[2 + 3 * i] - 5 + j,ldm[1 + 3 * i] - 5 + k]
                  count = count + 1
       
        
        if not rng == 0:
            # mean range
            rng = rng / count
            # id
            d.append(ldm[0 + 3 * i])
            #range
            d.append(rng)
            # bearing
            imgWidth = len(deepframe[1]) # 640
            targetWidth = - (ldm[1 + 3 * i] - imgWidth / 2) # esquerda+/direita-
            bearing = vvar.kinectAngle * targetWidth / imgWidth 
            d.append(bearing)
            #print bearing * 180 / math.pi
    
    msg.data = d
    return msg



def getFrame():
    newframe = vvar.colorImage
    newdepth = vvar.depthImage
    return newframe.copy(), newdepth.copy()



# MAIN
if __name__ == '__main__':
    try:
        # inicializacao do publisher                
        pub_land = rospy.Publisher('/processing/measurements', Float32MultiArray, queue_size=20)

        # inicializacao do subscriber
        rospy.Subscriber('/camera/depth/image', Image, GetDepth)
        rospy.Subscriber('/camera/rgb/image_color', Image, GetImage)
        
        # inicializacao do node
        rospy.init_node('detection', anonymous=True)

        # Mensagem dos landmarks measurements
        measMsg = Float32MultiArray()
        
        # Janela de tuning de cores 
        cv2.namedWindow("Control")
        cv2.createTrackbar("LowH", "Control", vvar.iLowH, 179, changeBarLH)
        cv2.createTrackbar("HighH", "Control", vvar.iHighH, 179, changeBarHH)

        cv2.createTrackbar("LowS", "Control", vvar.iLowS, 255, changeBarLS)
        cv2.createTrackbar("HighS", "Control", vvar.iHighS, 255, changeBarHS)

        cv2.createTrackbar("LowV", "Control", vvar.iLowV, 255, changeBarLV)
        cv2.createTrackbar("HighV", "Control", vvar.iHighV, 255, changeBarHV)
        cv2.waitKey(30)

        
        while not rospy.is_shutdown():        
            
            if vvar.receive == 1 and vvar.receiveDeep == 1:
                
                vvar.receive = 0
                
                # Recebe o frame mais recente
                currentframe, depthframe = getFrame()
                # Copia frame para depois colocar markers
                target = currentframe.copy()

                # Obter contornos de cada cor de interesse
                control, ccont = getContours('control',currentframe)   #Tuner      
                conBlu, cBlue = getContours('blue',currentframe)
                conPin, cPink = getContours('pink',currentframe)
                conYel, cYellow = getContours('yellow',currentframe)
                conWhi, cWhite = getContours('white',currentframe)

                # Analise dos contornos
                target, ldmPos = searchLD(conYel, conBlu, conPin, currentframe, target)
                
                #print len(depthframe), len(depthframe[0]), len(depthframe[1]),len(depthframe[2])
                
                #cv2.circle(depthframe,(ldmPos[1],ldmPos[2]), 15, (255,255,255), -1)
                # Distancia
                measurementDetermine(ldmPos, depthframe, measMsg)

                # Publica localizacoes                              
                # pub_land.publish(ldmMsg)
                # Publica measurements                              
                pub_land.publish(measMsg)
                
                # Mostrar Imagens
                cv2.imshow("Control", ccont)
                #cv2.imshow("White Contour", cWhite)
                #cv2.imshow("Blue Contour", cBlue)
                #cv2.imshow("Yellow Contour", cYellow)
                #cv2.imshow("Pink Contour", cPink)
                #cv2.imshow("Color", currentframe)
                #cv2.imshow("Depth",  depthframe)           
                cv2.imshow("Targets", target)
                cv2.waitKey(30)


            rate = rospy.Rate(20)
            rate.sleep()  
        
        
    except rospy.ROSInterruptException:
	     pass
        
