#!/usr/bin/env python

import random
import param

# M -> numero de particulas
# x -> posicao das abcissas
# y -> posicao das ordenadas
# t -> angulo theta de orientacao do robo
# w -> peso da particula

class PoseState:
    """Class com a estrutura de um estado"""
    

    def __init__(self, n_particulas = 0):
        self.m = n_particulas
        self.x = []
        self.y = []
        self.t = []
        self.w = []

        for i in range(self.m):        
            self.x[len(self.x):] = [random.uniform(param.xmin, param.xmax)]
            self.y[len(self.y):] = [random.uniform(param.ymin, param.ymax)]
            self.t[len(self.t):] = [random.uniform(param.tmin, param.tmax)]
            self.w[len(self.w):] = [1.0 / self.m]
        self._data_len = n_particulas * 4

    def get_n_particles():
        return self.m
        
    def __len__(self):
        return self._data_len

    def bestParticle(self):
        return self.w.index(max(self.w))

    def rosbustmean(self):
        epsX = 0.1
        epsY = 0.1
        epsT = 0.03
        
        wcorr = 0.0
        pose = [0,0,0]
        imax = self.bestParticle()
        for i in range(self.m):
            if abs(self.x[i]-self.x[imax])<epsX and abs(self.y[i]-self.y[imax])<epsY and abs(self.t[i]-self.t[imax])<epsT: 
                pose[0] = pose[0] + self.x[i] * self.w[i] 
                pose[1] = pose[1] + self.y[i] * self.w[i]
                pose[2] = pose[2] + self.t[i] * self.w[i]
                wcorr = wcorr + self.w[i]

        pose[0] = pose[0] / wcorr 
        pose[1] = pose[1] / wcorr
        pose[2] = pose[2] / wcorr
        return pose
         
   
