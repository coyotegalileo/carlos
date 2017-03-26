#!/usr/bin/env python

import param
import math
import numpy as np

# perception model
def perception(z, pose):
    
    # inicializa w
    w = 1.0;

    # Para cada landmark calcula probabilidade da mediacao
    for i in range(len(z)):
        q = get_prob(z[i],pose)
        w = w * q

    return w


def get_prob(zc,pose):

    # Get which feature is being observed (one per cicle)
    c = zc[2]    
    for i in range(len(param.feat)):
        if param.feat[i][2] == int(c):
            observed = param.feat[i]
            break

    # Extract position
    mx = observed[0]
    my = observed[1]

    # Get pose from input
    x = pose[0]
    y = pose[1]
    th = pose[2]

    # Get pose of the camera
    x = x + param.camera_offset * math.cos(th)
    y = y + param.camera_offset * math.sin(th)

    # Compute the range and bearing from pose to specified landmark
    rmap = math.sqrt((mx - x) * (mx - x) + (my - y) * (my - y))
    phimap = math.atan2(my-y, mx-x)

    # Difference between measure and belief
    pr = zc[0] - rmap
    pphi = zc[1]  - (phimap - th)
    pphi = pphi - math.floor((pphi+math.pi)/(2*math.pi))*(2*math.pi)
    pid = 0;

    # Variancias em funcao da distancia e bearing medidos
    rg_var = param.range_var + zc[0] * param.range_alpha
    br_var = param.bear_var * math.pi / 180 + abs(zc[1]) * param.bear_alpha * 180 / math.pi

    # Probability assuming independence and using normal pdf centered in 0
    q = prob_normal(pr, rg_var) * prob_normal(pphi, br_var) * prob_normal(pid,param.id_var)
    return q

def prob_normal(a,b):
    return (1 / (2 * math.pi * b)**0.5) * math.exp(-1 / 2 * a * a / b)
