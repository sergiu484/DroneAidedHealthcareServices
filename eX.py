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

Pi = {i: rnd.randint(1, 2) for i in I}
Di = {i: rnd.randint(1, 2) for i in I}


def Cost(a, b):
    return math.sqrt(pow(a[0][1] - b[0][1], 2) + pow(a[0][0] - b[0][0], 2))+a[1] - a[2] + b[1] - b[2]


def Eliminare(path1, path2):
    n1 = copy.deepcopy(path1)
    n2 = copy.deepcopy(path2)
    for i in path1:
        if i in path2:
            aux1 = copy.deepcopy(n1)
            aux2 = copy.deepcopy(n2)
            aux1.remove(i)
            aux2.remove(i)
            Puncte1 = [i[0] for i in n1]
            Puncte2 = [i[0] for i in n2]
            Incarcatura1 = [i[1] - i[2] for i in n1]
            Incarcatura2 = [i[1] - i[2] for i in n2]
            s1 = 0
            s2 = 0
            for i in Incarcatura1:
                s1 += i
            for i in Incarcatura2:
                s2 += i
            if ParteaOP.DistantaCale(Puncte1)+s1 <= ParteaOP.DistantaCale(Puncte2)+s2:
                n2 = aux2
            else:
                n1 = aux1
    path1 = n1
    path2 = n2
    return path1, path2


def ImpartireInCai(tur, limita, centru, Pi, Di):
    Cai = [[]]
    n = 0
    cale = []
    i = 0
    while i != len(tur):
        cale2 = copy.deepcopy(cale)
        cale2.append(tur[i])
        s = 0
        for j in cale2:
            s += Pi[j]-Di[j]
        if ParteaSP.distanta2Puncte(centru, cale2[0]) + ParteaOP.DistantaCale(cale2) + ParteaSP.distanta2Puncte(centru, cale2[-1]) <= limita and abs(s) <= limita:

            cale = cale2
            Cai[n] = cale
            i += 1

        else:
            if Cai[n] == []:
                print('cale----', centru, cale2, ParteaSP.distanta2Puncte(centru,
                                                                          cale2[0]) + ParteaOP.DistantaCale(cale2) + ParteaSP.distanta2Puncte(centru, cale2[-1]), cale)
                break
            cale = []
            Cai.append([])
            n += 1

        # print(Cai)
        # print(tur)
    return Cai


def MiniAco(nodes):
    world = pants.World(nodes, Cost)

    solver = pants.Solver()
    solution = solver.solve(world)
    # or
    solutions = solver.solutions(world)

    # print('distance',solution.distance)
    # print('tour',solution.tour)    # Nodes visited in order
    # print('path',solution.path)    # Edges taken in order
    # or
    best = float("inf")
    bestT = 0
    for solution in solutions:
        assert solution.distance < best
        best = solution.distance
        bestT = solution.tour
    # bestT.insert(0,centru)
    # bestT.append(centru)
    return bestT


def ACO(I, R, Raza, k, Pk, priceSmall, priceBig, Pi, Di):
    Ri = ParteaSP.CentrePacient(I, R, Raza)
    R1, Ri = ParteaSP.SP(R, Ri)
    PuncteInCentru = dict()
    for i in R1:
        PuncteInCentru[i] = []
        for j in I:
            d = ParteaSP.distanta2Puncte(i, j)
            if d <= Raza:
                PuncteInCentru[i].append((j, d))
        PuncteInCentru[i] = sorted(PuncteInCentru[i], key=lambda x: x[1])
    for i in R1:
        Pi[i] = 0
        Di[i] = 0
    bestCai = []
    for i in PuncteInCentru:
        for j in range(0, len(PuncteInCentru[i])):
            PuncteInCentru[i][j] = (
                PuncteInCentru[i][j][0], Pi[PuncteInCentru[i][j][0]], Di[PuncteInCentru[i][j][0]])
        bestCai.append(MiniAco(PuncteInCentru[i]))
    print(PuncteInCentru)
    print('bestCai1', bestCai)
    for i in range(0, len(bestCai)-1):
        for j in range(i+1, len(bestCai)):
            bestCai[i], bestCai[j] = Eliminare(bestCai[i], bestCai[j])
    for i in range(0, len(bestCai)):
        for j in range(0, len(bestCai[i])):
            bestCai[i][j] = bestCai[i][j][0]
    print('Best', bestCai)

    CaiFinale = []
    for i in range(0, len(R1)):
        Lista = ImpartireInCai(bestCai[i], Pk[1], R1[i], Pi, Di)
        for j in range(0, len(Lista)):
            Lista[j].insert(0, R1[i])
            Lista[j].append(R1[i])
            CaiFinale.append(Lista[j])
    print('CaiFinale', CaiFinale)
    for i in CaiFinale:
        d = ParteaOP.DistantaCale(i)
        print('D=', d)

    ClasificareCai = []
    nrBig = 0
    nrSmall = 0
    for i in CaiFinale:
        d = ParteaOP.DistantaCale(i)
        s = 0
        for j in i:
            s += Pi[j] - Di[j]
        if d > Pk[0] or abs(s) > Pk[0]:
            ClasificareCai.append([i, 1])
            nrBig += 1
        else:
            ClasificareCai.append([i, 0])
            nrSmall += 1

    print('Clasif', ClasificareCai)

    xCentruDronaInainteEliminare = [i[0] for i in R]
    yCentruDronaInainteEliminare = [i[1] for i in R]
    IdPuncte = dict()
    fig, ax = plt.subplots()
    # Desenul Razei Centrele de Drone Initiale, Cu negru
    for i in R:
        a_circle = plt.Circle(i, Raza, color='k', linewidth=0.5, fill=False)
        cercuri = ax.add_artist(a_circle)
    desenCoordonateCentruDrone1 = plt.scatter(xCentruDronaInainteEliminare, yCentruDronaInainteEliminare, c='k',
                                              marker='s')  # pune Centrele de Drone Inainte de Eliminare pe axa
    # desenCoordonateCentruDrone1.remove()

    # Coordonatele Centrele de Drona Dupa Eliminare
    xCentruDronaDupaEliminare = [i[0] for i in R1]
    yCentruDronaDupaEliminare = [i[1] for i in R1]
    # Desenul Razei Centrele de Drone dupa Eliminare Centrelor Redundante, Cu Rosu
    for i in R1:
        a_circle = plt.Circle(i, Raza, color='r', linewidth=0.5, fill=False)
        ax.add_artist(a_circle)
    desenCoordonateCentruDrone2 = plt.scatter(xCentruDronaDupaEliminare, yCentruDronaDupaEliminare, c='r',
                                              marker='s')  # pune Centrele de Drone Dupa Eliminare pe axa

    # setarea Raza Centrului de Drona sa incapa complet in imagine
    xlimMin = min(xCentruDronaDupaEliminare) - (Raza + 1)
    xlimMax = max(xCentruDronaDupaEliminare) + (Raza + 1)
    print("Maxim xCentruDrona = %d, Minim xCentruDrona = %d " %
          (xlimMax, xlimMin))

    ylimMin = min(yCentruDronaDupaEliminare) - (Raza + 1)
    ylimMax = max(yCentruDronaDupaEliminare) + (Raza + 1)
    print("Maxim yCentruDrona = %d, Minim yCentruDrona = %d " %
          (ylimMax, ylimMin))
    # Construirea Dimensiunei Imaginei
    ax.set(xlim=(xlimMin, xlimMax), ylim=(ylimMin, ylimMax))

    # Pacientii
    xPacient = [i[0] for i in I]
    yPacient = [i[1] for i in I]
    desenCoordonatePacienti = plt.scatter(
        xPacient, yPacient, c='b')  # pune pacientii pe axa
    # numerotam pacientii
    n = 1
    for xy in zip(xPacient, yPacient):
        plt.annotate("p%d" % (n), xy=xy, textcoords='data')
        IdPuncte[xy] = "p%d" % (n)
        n += 1

    # Numerotam Centrele de Drona Inainte Eliminare
    n = 1
    for xy in zip(xCentruDronaInainteEliminare, yCentruDronaInainteEliminare):
        numerotareCentreDrona = plt.annotate(
            "D%d" % (n), xy=xy, textcoords='data')
        IdPuncte[xy] = "D%d" % (n)
        n += 1
    print("Id=", IdPuncte)

    for i in ClasificareCai:
        j = i[0]
        c = i[1]
        if c == 0:
            # deseneaza calea pentru drona de Tip 1
            nrSmall += 1
            for z in range(0, len(j)-1):
                #plt.plot([j[z][0],j[z+1][0]],[j[z][1],j[z+1][1]],c = 'g', alpha = 0.6)
                plt.annotate('', xy=(j[z+1][0], j[z+1][1]), xycoords='data',
                             xytext=(j[z][0], j[z][1]), textcoords='data',
                             arrowprops=dict(frac=0.1, headwidth=5., width=0.5, color="g"))
                # print("j[z][0]=", j[z][0], "j[z][1]", j[z][1], "j[z+1][0]", j[z+1][0], "j[z+1][1]", j[z+1][1])
                # print(j[z], j[z+1], j)
        elif c == 1:
            # deseneaza calea pentru drona de tip2
            nrBig += 1
            for z in range(0, len(j)-1):
                #plt.plot([j[z][0],j[z+1][0]],[j[z][1],j[z+1][1]],c = 'y', alpha = 0.6)
                plt.annotate('', xy=(j[z + 1][0], j[z + 1][1]), xycoords='data',
                             xytext=(j[z][0], j[z][1]), textcoords='data',
                             arrowprops=dict(frac=0.1, headwidth=5., width=0.5, color="y"))
    # Salveaza desenul
    plt.savefig(os.path.join('.', 'ant1.png'), bbox_inches='tight')
    plt.close()

    fig, ax = plt.subplots()
    print('R1=', R1)
    for i in R1:
        a_circle = plt.Circle(i, Raza, color='r', linewidth=0.5, fill=False)
        ax.add_artist(a_circle)
    desenCoordonateCentruDrone2 = plt.scatter(xCentruDronaDupaEliminare, yCentruDronaDupaEliminare, c='r',
                                              marker='s')  # pune Centrele de Drone Dupa Eliminare pe axa
    # Construirea Dimensiunei Imaginei
    ax.set(xlim=(xlimMin, xlimMax), ylim=(ylimMin, ylimMax))
    desenCoordonatePacienti = plt.scatter(xPacient, yPacient, c='b')
    n = 1
    for xy in zip(xPacient, yPacient):
        plt.annotate("p%d" % (n), xy=xy, textcoords='data')
        n += 1
    n = 1
    for xy in zip(xCentruDronaInainteEliminare, yCentruDronaInainteEliminare):
        if xy in R1:
            numerotareCentreDrona = plt.annotate(
                "D%d" % (n), xy=xy, textcoords='data')
        n += 1
    # ==
    for i in ClasificareCai:
        j = i[0]
        c = i[1]
        if c == 0:
            # deseneaza calea pentru drona de Tip 1
            for z in range(0, len(j)-1):
                #plt.plot([j[z][0],j[z+1][0]],[j[z][1],j[z+1][1]],c = 'g', alpha = 0.6)
                plt.annotate('', xy=(j[z+1][0], j[z+1][1]), xycoords='data',
                             xytext=(j[z][0], j[z][1]), textcoords='data',
                             arrowprops=dict(frac=0.1, headwidth=5., width=0.5, color="g"))
                # print("j[z][0]=", j[z][0], "j[z][1]", j[z][1], "j[z+1][0]", j[z+1][0], "j[z+1][1]", j[z+1][1])
                # print(j[z], j[z+1], j)
        elif c == 1:
            # deseneaza calea pentru drona de tip2
            for z in range(0, len(j)-1):
                #plt.plot([j[z][0],j[z+1][0]],[j[z][1],j[z+1][1]],c = 'y', alpha = 0.6)
                plt.annotate('', xy=(j[z + 1][0], j[z + 1][1]), xycoords='data',
                             xytext=(j[z][0], j[z][1]), textcoords='data',
                             arrowprops=dict(frac=0.1, headwidth=5., width=0.5, color="y"))

    plt.savefig(os.path.join('.', 'ant2.png'), bbox_inches='tight')
    plt.show()
    plt.close()
    DateTabel = dict()
    PretCentru = dict()
    TipDroneCentru = dict()
    print('TABEL', ClasificareCai)
    for i in ClasificareCai:
        DateTabel[IdPuncte[i[0][0]]] = []
        PretCentru[IdPuncte[i[0][0]]] = 0
        TipDroneCentru[IdPuncte[i[0][0]]] = [0, 0]
    NrDroneMici = 0
    NrDroneMari = 0
    DistantaTotala = 0
    PretTotal = 0

    for i in ClasificareCai:
        if i[1] == 0:
            NrDroneMici += 1
            TipDroneCentru[IdPuncte[i[0][0]]][0] += 1
            PretCentru[IdPuncte[i[0][0]]] += priceSmall
            PretTotal += priceSmall
        else:
            NrDroneMari += 1
            TipDroneCentru[IdPuncte[i[0][0]]][1] += 1
            PretCentru[IdPuncte[i[0][0]]] += priceBig
            PretTotal += priceBig
        DistantaPath = ParteaOP.DistantaCale(i[0])

        DateTabel[IdPuncte[i[0][0]]].append([i[0], DistantaPath])

        DistantaTotala += DistantaPath

    for i in DateTabel.keys():
        for z in range(0, len(DateTabel[i])):
            for j in range(0, len(DateTabel[i][z][0])):
                DateTabel[i][z][0][j] = IdPuncte[DateTabel[i][z][0][j]]
            DateTabel[i][z][1] = round(DateTabel[i][z][1], 2)

    print(DateTabel)
    print(DistantaTotala, NrDroneMici, NrDroneMari, PretTotal)
    print(PretCentru)
    print(TipDroneCentru)
    print('Clasif ', ClasificareCai)
    return DateTabel, PretCentru, TipDroneCentru, DistantaTotala, NrDroneMici, NrDroneMari, PretTotal, IdPuncte, len(I)

    # MiniAco(R1+I)


ACO(I, R, Raza, k, Pk, costLow, costBig, Pi, Di)


nodes = []
for _ in range(20):
    x = random.uniform(-10, 10)
    y = random.uniform(-10, 10)
    nodes.append((x, y))
