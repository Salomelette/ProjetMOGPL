#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 18:42:57 2018

@author: 3520413
"""

#from gurobipy import *
#import numpy as np

#recuperation du nombre de villes 
f = open("/users/Etu3/3520413/mogpl/projet/Data/villes92.txt")

n=0
for data in f:
    #print(data)
    n+=1
    
f.close()

#recuperation des distances
f = open("/users/Etu3/3520413/mogpl/projet/Data/distances92.txt")

dij=[]
for data in f:
    if type(data)=<class 'str'>:
        for j in range(n):
            
    


#m1 = model("question1")
#
#X = []
#J = [2,5,14]
#k = 3
#a = 0.1
#
#for i in range(k):
#    for j in range(n):
#        aux = []
#        aux.append(m1.addVar(vtype=GRB.BINARY))
#    X.append(aux)
#    
#m1.update()
#
#fo = LinExpr()
#fo = 0
#
#for i in range(n):
#    for j in range(k):
#        fo+=d[i][J[j]]*X[i][j]
#        
#m1.setObjective(obj,GRB.MAXIMIZE)
#
#for i in range(n):
#    s = 0
#    for j in range(k):
#        s+=X[i][j] #correspond a la somme des xij sur j 
#        
#    m1.addConstr(s=1) #contrainte 1: une ville appartient à un unique secteur
#    
#for j in range(k):
#    s1=0
#    s2=0
#    for i in range(n):
#        s1+=X[i][j]*v[i] #somme des populations totales des villes composant un secteur
#        s2+=v[i] #somme des populations totales des villes
#    
#    m1.addConstr((s1/s2)<=((1+a)/k)) #contrainte 2: populations totales des villes composant un secteur ne doit pas dépasser gamma (voir poly)

        
    
        
