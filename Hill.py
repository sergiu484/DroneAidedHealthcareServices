import random
import math
import pants
import ParteaOP
import ParteaSP
import wx
import os
import matplotlib.pyplot as plt
import copy
import itertools
import numpy as np
# import pandas as pd
rnd = np.random
rnd.seed(0)


I, R, Raza, k, Pk, costLow, costBig = ParteaOP.citire("fileBig_5.txt")


def CelMaiAproapePunct(Punct, Puncte, I):
    minim = - 1
    P2 = 0
    for i in Puncte:
        if i[0] != Punct and i[0] in I:
            d = ParteaSP.distanta2Puncte(i[0], Punct)
            if d < minim or minim == -1:
                P2 = i[0]
    return P2


def Cale(Cai, Centru, DistantaIncrc, PuncteInCentru, Pi, Di, I):
    dis = 0
    inc = 0
    cale = [[Centru], 0]
    last = Centru
    ok = 0
    while ok == 0:
        posibil = CelMaiAproapePunct(last, PuncteInCentru[Centru], I)
        if posibil == 0:
            ok = 1
        else:
            dis += ParteaSP.distanta2Puncte(last, posibil)
            inc += Pi[posibil] - Di[posibil]
            if dis + ParteaSP.distanta2Puncte(posibil, Centru) > DistantaIncrc[1] or inc > DistantaIncrc[1] or dis > DistantaIncrc[1]:
                ok = 1
            else:
                cale[0].append(posibil)
                last = posibil
                I.remove(posibil)

    cale[0].append(Centru)
    dis = DistantaCale(cale[0])
    cale[0].reverse()

    if dis > DistantaIncrc[0] or inc > DistantaIncrc[0]:
        cale[1] = 1

    print('Isize', len(I))
    if (len(cale[0]) > 2):
        Cai.append(cale)
    print(Cai)


def GenerareCai(permutare, Cai, DistantaIncrc, PuncteInCentru, Pi, Di, I, Centre):
    while I != []:
        print('Isize2', len(I))
        for i in permutare:
            print('pass1')
            Cale(Cai, Centre[[i][0]], DistantaIncrc, PuncteInCentru, Pi, Di, I)


def Optimizare(permutari, Cai, DistantaIncrc, PuncteInCentru, Pi, Di, I, Centre):
    I2 = copy.deepcopy(I)
    Cai2 = copy.deepcopy(Cai)
    for i in permutari:
        GenerareCai(i, Cai2, DistantaIncrc, PuncteInCentru, Pi, Di, I2, Centre)
        if len(Cai2) < len(Cai) or len(Cai) == 0:
            Cai = Cai2
    return Cai


def DistantaCale(cale):
    d = 0
    print(cale)
    for i in range(0, len(cale)-1):
        d += ParteaSP.distanta2Puncte(cale[i], cale[i+1])
    return d


nodes = []
for _ in range(10):
    x = random.uniform(-10, 10)
    y = random.uniform(-10, 10)
    nodes.append((x, y))

Pi = {i: rnd.randint(1, 2) for i in nodes}
Di = {i: rnd.randint(1, 2) for i in nodes}
fig, ax = plt.subplots()

for i in nodes:
    plt.scatter(
        i[0], i[1], c='b', marker='s')

plt.scatter(
    0, 0, c='r', marker='s')

nodes2 = copy.copy(nodes)

PuncteInCentru = dict()
PuncteInCentru[(0, 0)] = []
for i in nodes:
    PuncteInCentru[(0, 0)].append((i, ParteaSP.distanta2Puncte((0, 0), i)))
p = [([0])]
print(p[0])
cai = Optimizare([([0])], [], [15, 30], PuncteInCentru,
                 Pi, Di, nodes2, [(0, 0)])
print('Cai ', cai, len(cai))
for i in range(0, len(cai)):
    print(cai[i])
    for j in range(0, len(cai[i][0])-1):
        print(cai[i][0][j])
        plt.plot([cai[i][0][j][0], cai[i][0][j+1][0]],
                 [cai[i][0][j][1], cai[i][0][j+1][1]], c="y")

plt.show()
