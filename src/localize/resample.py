#!/usr/bin/env python

import param
import random
import math
from state import PoseState

# reasampling algorithms

# Select with replacement
def resample(state):
    # a soma dos pesos tem que vir igual a 1
    w = [state.w[0]]
    # novo vector de pesos com o valor cumulativo
    for i in range(1,param.M):
        w[len(w):] = [w[i-1] + state.w[i]]
    # numeros aleatorios que vao decidir que particulas continuam
    r = []
    for i in range(param.M+1):
        r[len(r):] = [random.random()]
    r.sort()
    # determinar quais e quantas particulas de cada continuam
    index = [] #indices das que avancam 
    r[param.M] = 1
    i = 0
    j = 0
    # o vector index fica com os indices das variaveis a passar
    while i < param.M:
        if r[i] < w[j]:
            index[len(index):] = [j]
            i = i + 1
        else:
            j = j + 1
    # novas particulas sao geradas
    x = []
    y = []
    t = []
    w = []
    for i in range(param.M):
        x[len(x):] = [ state.x[index[i]] ]
        y[len(y):] = [ state.y[index[i]] ]
        t[len(t):] = [ state.t[index[i]] ]
        w[len(w):] = [ 1.0 / param.M ]
    
    state.x = x
    state.y = y
    state.t = t
    state.w = w
    return state


# Low Variance Re-sampling
def low_var_resample(state):
    # novas particulas sao geradas
    x = []
    y = []
    t = []
    w = []

    r = random.uniform(0, 1.0/param.M)
    c = state.w[0]
    i = 0
    for m in range (param.M):
        u = r + m * 1.0 / param.M
        while u > c:
            i = i + 1
            c = c + state.w[i]
        # Preenchimento das particulas
        x[len(x):] = [ state.x[i]]
        y[len(y):] = [ state.y[i]]
        t[len(t):] = [ state.t[i]]
        w[len(w):] = [ 1.0 / param.M ]
    # Attribuicao ao novo estado
    state.x = x
    state.y = y
    state.t = t
    state.w = w
    return state

# calcula numero de pariculas efectivas
def eff_particles(w):
    neff = 0
    for i in range(param.M):
        neff = neff + w[i] * w[i]
    neff = 1 / neff
    return neff

def kidnap_resample(state, randomprob, z):
    # novas particulas sao geradas
    x = []
    y = []
    t = []
    w = []
    
    # Seed e inicializacoes
    r = random.uniform(0, 1.0/param.M)
    c = state.w[0]
    i = 0
    
    # Ciclo de Resampling 
    for m in range (param.M):
        kidnap =  random.uniform(0.0 , 1.0)
        u = r + m * 1.0 / param.M
        while u > c:
            i = i + 1
            c = c + state.w[i]
        # Possibilidade de random
        if kidnap < randomprob and len(z) > 0:
            landmark = random.choice(range(len(z)))
    
            # TODO Sample com base em mais que uma mediacao
            pose = sample_pose(z[landmark])
            x[len(x):] = [ pose[0] ]
            y[len(y):] = [ pose[1] ]
            t[len(t):] = [ pose[2] ]
            w[len(w):] = [ 1.0 / param.M ]

        else:
            # Preenchimento das particulas
            x[len(x):] = [ state.x[i]]
            y[len(y):] = [ state.y[i]]
            t[len(t):] = [ state.t[i]]
            w[len(w):] = [ 1.0 ]


    # Attribuicao ao novo estado
    state.x = x
    state.y = y
    state.t = t
    state.w = w

    return state

# Sample de uma pose com base numa mediacao
def sample_pose(measured):
     
    # Extracao de parametros da observacao
    rg_i = measured[0] 
    phi_i = measured[1]
    id_i = measured[2]

    # Extracao dos parametros do landmark
    for i in range(len(param.feat)):
        if param.feat[i][2] == int(id_i):
            observed = param.feat[i]
            break

    # Extract position of landmark
    mx = observed[0]
    my = observed[1]

    # Variancias em funcao da distancia e bearing medidos
    rg_var = param.range_var + rg_i * param.range_alpha
    br_var = param.bear_var * math.pi / 180 + abs(phi_i) * param.bear_alpha * 180 / math.pi

    # Sampling Gassiano
    t0 = random.uniform(0,2*math.pi)
    rg = rg_i + sample_pdf(rg_var)
    phi = phi_i + sample_pdf(br_var)
    
    # Pose do sample
    x = mx + rg * math.cos(t0)
    y = my + rg * math.sin(t0)
    th = t0 - math.pi - phi

    return [x ,y ,th]

# Sample de uma Gaussiana centrada em 0 com variancia var
def sample_pdf(var):
    rand = 0    
    for i in range(12):
        rand = rand + random.uniform(-1,1)
    return var / 6 * rand





