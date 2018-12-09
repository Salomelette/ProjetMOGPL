#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 14:56:06 2018

@author: salom
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 19:20:02 2018

@author: 3520413
"""

from gurobipy import *
import numpy as np
import re
import matplotlib.image as mpimg

#recuperation du nombre de villes 
f = open("/home/salom/mogpl/projet/Data/villes92.txt")

n=0
for data in f:
    n+=1
    
f.close()
            
    
#recuperation des distances
f = open("/home/salom/mogpl/projet/Data/distances92.txt")

dij = []
file = f.read().splitlines()
for i in range(len(file)):
    if type(file[i]) == str:
        aux = []
        for j in range(1,n+1):
            file[i+j] = float(file[i+j])
            aux.append(file[i+j]) 
        dij.append(aux)
        
f.close()
        
#recuperation des populations totales 
f = open("/home/salom/mogpl/projet/Data/populations92.txt")

vi=[]
for data in f:
    d=re.findall('\d+', data)[0] 
    vi.append(int(d))


m3 = Model("question3")
m3.setParam('OutputFlag',False)

X = []
Y = []
k = 3
a = 0.1
eps = 1e-6

for i in range(n):
    aux = []
    for j in range(n):
        aux.append(m3.addVar(vtype=GRB.BINARY))
    X.append(aux)
  
for i in range(n):
    Y.append(m3.addVar(vtype=GRB.BINARY))

z = m3.addVar(vtype=GRB.CONTINUOUS,lb=0,obj=1.0)
    
m3.update()

fo = LinExpr()
fo = z

for i in range(n):
    for j in range(n):
        fo+=dij[i][j]*X[i][j]*eps
        
m3.setObjective(fo,GRB.MINIMIZE)

for i in range(n):
    s = 0
    for j in range(n):
        s+=X[i][j] #correspond a la somme des xij sur j 
        
    m3.addConstr(s, GRB.EQUAL, 1) #contrainte 1: une ville appartient à un unique secteur
    
for j in range(n):
    s1=0
    s2=0
    for i in range(n):
        s1+=X[i][j]*vi[i] #somme des populations totales des villes composant un secteur
        s2+=vi[i] #somme des populations totales des villes
    
    m3.addConstr((s1/s2)<=((1+a)/k)) #contrainte 2: populations totales des villes composant un secteur ne doit pas dépasser gamma (voir poly)


for i in range(n):
    s = 0
    for j in range(n):
        s+=X[i][j]*dij[i][j]
    
    m3.addConstr(s<=z) #contrainte 3: z doit correspondre au max des sommes  
    
for j in range(n):
    s = 0
    for i in range(n):
        s+=X[i][j] #correspond a la somme des xij sur i 
        
    m3.addConstr(s-Y[j]*n<=0) #contrainte 4: une ville ne doit pas être associée à une ville n'étant pas une ressource 
#    
    
#for j in range(n):
#    m3.addConstr(sum(X[:,j])-Y[j]*n<=0) #contrainte 4: une ville ne doit pas être associée à une ville n'étant pas une ressource
    
m3.addConstr(sum(Y) == k) #contrainte 5: il doit y avoir k secteurs 
    
m3.optimize()

x = np.array(m3.x[:-(n+1)]).reshape(n,n)
y = np.array(m3.x[n*n:-1])

J = []
for i in range(len(Y)):
    if Y[i].x == 1: 
        J.append(i)

maxdij = 0
moy = 0

print(y,J)

for i in range(n):
    for j in range(n):
        moy += x[i][j]*dij[i][j]
        if x[i][j] == 1 and dij[i][j] > maxdij :
            maxdij = dij[i][j]         

print ("Valeur de la fonction objectif =" , m3.ObjVal)
print ("Matrice des xij :\n" , x)
print ("Satisfaction moyenne =" , moy/n)
print ("Satisfaction du maire le moins bien servi =" , maxdij)

#récupération de la carte
img = mpimg.imread("./Data/92.png")

#récupération des coordonnées de chaque ville
f = open("/home/salom/mogpl/projet/Data/coordvilles92.txt")

coord_i=[]
for data in f:
    la = re.findall('\d+', data)[0]
    lo = re.findall('\d+', data)[1]
    coord_i.append((int(la),int(lo)))

#affichage sur la carte
colors = [ (300, 0, 0), (0, 300, 0), (0, 0, 300), (177, 0, 177), (0, 177, 177) ]   #rouge, vert, bleu, violet, turquoise
for i in range(n):
    for j in range(n):
        if x[i][j] == 1:
            la, lo = coord_i[i]
            img[lo,la] = colors[J.index(j)]
            for c in range(-3,4):
                for r in range(-3,4):
                    img[lo+c,la+r] = colors[J.index(j)]
            if i in J:
                for c in range(-5,5):
                    img[lo,la+c] = (0, 0, 0)
#                   img[lo,la-5] = colors[j]
                    img[lo+c,la] = (0, 0, 0)
#                   img[lo-5,la] = colors[j]
#        elif X[i][j].x == 1 and i in J:
#            la, lo = coord_i[i]
#            img[lo,la] = colors[j]
            
            
mpimg.imsave("res3_k="+str(k)+"_a="+str(a)+".png", img)