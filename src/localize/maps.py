#!/usr/bin/env python

import param
import math


# Obter frame actual
def getMap():
    newmap = param.mapa
    return newmap

# Verifica se pose esta no mapa
def mapa(xm, ym):
    # para ja so 1 ou 0    
    dentro = True
    
    if param.mapreceive: 
        dentro = check_coord(xm,ym)

    if dentro:
        return 1
    else:
        return 0
# Funcao onde colocar o mapa
def check_coord(xm,ym):
    
    mapa = getMap()
    res = mapa.info.resolution
    width =  mapa.info.width
    
    xcell =  math.floor(xm / res)
    ycell =  math.floor(ym / res)

    if mapa.data[int(xcell + ycell * width)] < 50 :
        return False
    
    return True
