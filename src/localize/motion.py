#!/usr/bin/env python
# coding=utf-8

import random
import numpy as np
import math
import param as p

#Sample motion model
#Inputs: Uma das partículas no instante t-1; Leituras da odometria
def motion(u_x, u_y, u_teta, x, y, teta): 
  

    # O que o robot rodou para ficar na direção em que andou 
    rot1_odo = math.atan2(u_y[1] - u_y[0], u_x[1] - u_x[0]) - u_teta[0]    
    rot1_odo = rot1_odo - math.floor((rot1_odo + math.pi)/ (2 * math.pi)) * 2  * math.pi
       

    # Translaçao estimada pela odometria
    trans_odo = math.sqrt(math.pow(u_x[1] - u_x[0] ,2) + math.pow(u_y[1] - u_y[0] ,2))  

    # O que o robot rodou depois de parar na posiçao final    
    rot2_odo = u_teta[1] - u_teta[0] - rot1_odo  
    rot2_odo = rot2_odo - math.floor((rot2_odo + math.pi)/ (2 * math.pi)) * 2  * math.pi
       
 # entre -pi e pi                                           
    #print rot1_odo,rot2_odo, (rot1_odo + rot2_odo)
    #print u_x, u_y, u_teta, x, y, teta

 
    r12 = (rot1_odo + rot2_odo)
    if abs(r12) > math.pi:
        r12 = 2* math.pi - abs(r12)        

    # Variancias do ruido
    var1 = abs(p.a1 * rot1_odo) + abs(p.a2 * trans_odo)
    var2 = abs(p.a3 * trans_odo) + abs(p.a4 * (r12))
    var3 = abs(p.a1 * rot2_odo) + abs(p.a2 * trans_odo) 

    #Falta importancia dos erros correcta


    # TODO verificar se isto e mesmo necessario num caso normal
    # para nao permitir que variancia seja zero 
    if  var1 != 0:
        rot1 = rot1_odo - np.random.normal(0, var1)                  
    else: 
        rot1 = rot1_odo

    if  var2 != 0:
        trans = trans_odo - np.random.normal(0, var2)                 
    else:
        trans = trans_odo

    if  var3 != 0:
        rot2 = rot2_odo - np.random.normal(0, var3)  
    else:    
        rot2 = rot2_odo
      
    # Mudar depois quando se incorporar os erros
    x_final = x + trans * math.cos(teta + rot1)
    y_final = y + trans * math.sin(teta + rot1)
    teta_final = teta + rot1 + rot2
    teta_final = teta_final - math.floor((teta_final )/ (2 * math.pi)) * 2  * math.pi
       

    return x_final, y_final, teta_final
