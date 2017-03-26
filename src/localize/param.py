#!/usr/bin/env python

import math
from nav_msgs.msg import Odometry
from nav_msgs.msg import OccupancyGrid

#### numero de particulas
M = 2000

#### Mapa 
# Definicao de limites iniciais
# Maximo
xmax = 6 #7.6
ymax = 6 #-1.35

# Minimo
xmin = -6   #7.6
ymin = -6   #-1.35

#### Gama de rotacao
tmin = 0.0              
tmax = 2.0 * math.pi 

mapa = OccupancyGrid()
mapreceive = False
#### Landmarks
feat = []

# Primeiro Circuito Sem medidas 
#feat.append([ 1.45, 3.9, 1])  # 1 WYP
#feat.append([ 0.0, 1.6, 3])  # 3 WPY
#feat.append([ 0.0, 0.0, 2])  # 2 WBP
#feat.append([ -0.25, 3.95, 4]) # 4 WPB

# Segundo Circuito Com Medidas Approx
feat.append([ 4.0, 1.29, 1])  # 1 WYP
feat.append([ 0.0, 0.0, 3])  # 3 WPY
feat.append([ 2.0, 1.65, 2])  # 2 WBP
feat.append([0.0, 2.85, 4]) # 4 WPB

#feat.append([ -0.378, 4.624, 1])  # 1 WYP
#feat.append([ 14.130, -9.8, 3])  # 3 WPY
#feat.append([ -0.36, -8.1, 2])  # 2 WBP
#feat.append([14.213, 6.24, 4]) # 4 WPB

# Teste de medicoes
#feat.append([ 0.0, 0.0, 1])  # 1 WYP
#feat.append([ 110.0, 0.0, 3])  # 3 WPY
#feat.append([0.30, 0.0, 2])  # 2 WBP
#feat.append([-0.30, 0.0, 4]) # 4 WPB

#### Odmometria
odometry = Odometry()

#### Obseervacoes
measure = []

#### Variancias
# Motion Model
a1 =   0.010738  #0.005   # Rotacoes em rotacoes
a2 =   0.003126  #0.07    # Translacao em rotacoes
a3 =   0.12132   #0.4    # Tranlacao em translacao
a4 =   0.013046  #0.2    # Rotacoes em Translacao

# Peception Model
range_var = 0.4     # metros
range_alpha = 0.0   # metros por metro
bear_var = 2        # graus
bear_alpha = 0.0    # graus por grau
id_var = 0.01       # ver como quantificar TODO

camera_offset = 0.15

### Kidnaped
wslow = 0
wfast = 0
alphaslow = 0.8
alphafast = 0.81


