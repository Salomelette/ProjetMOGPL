#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 14:13:58 2018

@author: salom
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


m1 = Model("question1")
m1.setParam('OutputFlag',False)

X = []
J = [2,5,14,7,30]
k = 3
a = 0.1

for i in range(n):
    aux = []
    for j in range(k):
        aux.append(m1.addVar(vtype=GRB.BINARY))
    X.append(aux)

# print(vi)
    
#recuperation du minimum de f(x)
m1.update()

fo = LinExpr()
fo = 0

for i in range(n):
    for j in range(k):
        fo+=dij[i][J[j]]*X[i][j]
        
m1.setObjective(fo,GRB.MINIMIZE)

for i in range(n):
    s = 0
    for j in range(k):
        s+=X[i][j] #correspond a la somme des xij sur j 
        
    m1.addConstr(s, GRB.EQUAL, 1) #contrainte 1: une ville appartient à un unique secteur
    
for j in range(k):
    s1=0
    s2=0
    for i in range(n):
        s1+=X[i][j]*vi[i] #somme des populations totales des villes composant un secteur
        s2+=vi[i] #somme des populations totales des villes
    
    m1.addConstr((s1/s2)<=((1+a)/k)) #contrainte 2: populations totales des villes composant un secteur ne doit pas dépasser gamma (voir poly)


for j in range(k):
    s = 0
    for i in range(n):
        s+=X[i][j] #correspond a la somme des xij sur j 
        
    m1.addConstr(s>=1)
     
m1.optimize()

X1 = np.array(m1.X).reshape(n,k)

#recuperation du minimum de g(x)
m2 = Model("question2")
m2.setParam('OutputFlag',False)

X = []
J = [2,5,14]
k = 3
a = 0.1
eps = 1e-6

for i in range(n):
    aux = []
    for j in range(k):
        aux.append(m2.addVar(vtype=GRB.BINARY))
    X.append(aux)

z = m2.addVar(vtype=GRB.CONTINUOUS,lb=0,obj=1.0)
    
m2.update()

fo = LinExpr()
fo = z

for i in range(n):
    for j in range(k):
        fo+=dij[i][J[j]]*X[i][j]*eps
        
m2.setObjective(fo,GRB.MINIMIZE)

for i in range(n):
    s = 0
    for j in range(k):
        s+=X[i][j] #correspond a la somme des xij sur j 
        
    m2.addConstr(s, GRB.EQUAL, 1) #contrainte 1: une ville appartient à un unique secteur
    
for j in range(k):
    s1=0
    s2=0
    for i in range(n):
        s1+=X[i][j]*vi[i] #somme des populations totales des villes composant un secteur
        s2+=vi[i] #somme des populations totales des villes
    
    m2.addConstr((s1/s2)<=((1+a)/k)) #contrainte 2: populations totales des villes composant un secteur ne doit pas dépasser gamma (voir poly)


for j in range(k):
    s = 0
    for i in range(n):
        s+=X[i][j] #correspond a la somme des xij sur i 
        
    m2.addConstr(s>=1)

for i in range(n):
    s = 0
    for j in range(k):
        s+=X[i][j]*dij[i][J[j]]
    
    m2.addConstr(s<=z)
    
     
m2.optimize()

X2 = np.array(m2.x[:-1]).reshape(n,k)

#calcul de PE
xg = 0.0
for i in range(n):
    for j in range(k):
        xg += X2[i][j]*dij[i][J[j]]

PE = 1.0 - m1.ObjVal/xg 

print(PE)        
        

