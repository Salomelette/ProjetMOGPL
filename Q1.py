#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 18:42:57 2018

@author: 3520413
"""

from gurobipy import *
import numpy as np
import re

#recuperation du nombre de villes 
f = open("/users/Etu3/3520413/mogpl/projet/Data/villes92.txt")

n=0
for data in f:
    n+=1
    
f.close()
            
    
#recuperation des distances
f = open("/users/Etu3/3520413/mogpl/projet/Data/distances92.txt")

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
f = open("/users/Etu3/3520413/mogpl/projet/Data/populations92.txt")

vi=[]
for data in f:
    d=re.findall('\d+', data)[0] 
    vi.append(int(d))


m1 = Model("question1")

X = []
J = [2,5,14]
k = 3
a = 0.1

for i in range(k):
    aux = []
    for j in range(n):
        aux.append(m1.addVar(vtype=GRB.BINARY))
    X.append(aux)

print(vi)
    
m1.update()

fo = LinExpr()
fo = 0

for j in range(n):
    for i in range(k):
        fo+=dij[i][J[i]]*X[i][j]
        
m1.setObjective(fo,GRB.MAXIMIZE)

for i in range(n):
    s = 0
    for j in range(k):
        s+=X[i][j] #correspond a la somme des xij sur j 
        
    m1.addConstr(s=1) #contrainte 1: une ville appartient à un unique secteur
    
for j in range(k):
    s1=0
    s2=0
    for i in range(n):
        s1+=X[j][i]*vi[i] #somme des populations totales des villes composant un secteur
        s2+=vi[i] #somme des populations totales des villes
    
    m1.addConstr((s1/s2)<=((1+a)/k)) #contrainte 2: populations totales des villes composant un secteur ne doit pas dépasser gamma (voir poly)


m1.optimize()
        
        
    
        
