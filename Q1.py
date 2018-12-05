#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 18:42:57 2018

@author: 3520413
"""

from gurobipy import *
import numpy as np
import re
import matplotlib.image as mpimg

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

min = 0

for i in range(n):
    for j in range(k):
        if X[i][j].x == 1 and d[i][j] < min :
            min = d[i][j]         

print "Valeur de la fonction objectif =" , m1.ObjVal
print "Matrice des xij :\n" , m1.X
print "Satisfaction moyenne =" , m1.ObjVal/n
print "Satisfaction du maire le moins bien servi =" , min

#récupération de la carte
img = mpimg.imread("./Data/92.png")

#récupération des coordonnées de chaque ville
f = open("/users/Etu3/3520413/mogpl/projet/Data/villes92.txt")

coord_i=[]
for data in f:
    la = re.findall('\d+', data)[0]
    lo = re.findall('\d+', data)[1]
    coord_i.append((la,lo)))

#affichage sur la carte
colors = [ (355, 0, 0), (0, 355, 0), (0, 0, 355), (177, 0, 177), (0, 177, 177) ]   #rouge, vert, bleu, violet, turquoise
for i in range(n):
    for j in range(k):
        if X[i][j].x == 1 and i not in J:
            la, lo = coord_i[i]
            img[lo,la] = colors[j]
            for c in range(1,4):
                img[lo+c,lo] = colors[j]
                img[la,lo+c] = colors[j]
                img[la-c,lo] = colors[j]
                img[la,lo-c] = colors
        elif X[i][j].x == 1 and i in J:
            la, lo = coord_i[i]
            img[lo,la] = colors[j]
            
            
mpimg.imsave("res_k=3_a=0,1.png", img)




        
        
    
        
