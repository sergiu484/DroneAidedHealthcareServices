from docplex.mp.model import Model
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.artist import Artist
import ParteaSP
import copy
import itertools
import pants
import math
import random

rnd = np.random
rnd.seed(0)


def citire(path):
    f = open(path)
    s1 = f.readline()[0:-1]
    s2 = f.readline()[0:-1]
    s3 = f.readline()[0:-1]
    s4 = f.readline()[0:-1]
    s5 = f.readline()[0:-1]
    s6 = f.readline()[0:-1]
    s7 = f.readline()[0:-1]
    f.close()
    l1 = s1.split(' ')
    l2 = s2.split(' ')
    l4 = s4.split(' ')
    l5 = s5.split(' ')
    c1 = []
    c2 = []
    c4 = []
    c5 = []

    for i in l1:
        c1.append((int(i.split(',')[0]), int(i.split(',')[1])))
    for i in l2:
        c2.append((int(i.split(',')[0]), int(i.split(',')[1])))
    c3 = int(s3)
    c6 = int(s6)
    c7 = int(s7)
    for i in l4:
        # c4 = Drona de tip 1 & Drona de tip 2
        c4.append(int(i.split(',')[0]))
        c4.append(int(i.split(',')[1]))
    for i in l5:
        c5.append(int(i.split(',')[0]))
        c5.append(int(i.split(',')[1]))
    return c1, c2, c3, c4, c5, c6, c7
# Setul de pacienti care ii folosim
#I = [(10,-5),(6,-3),(2,8),(9,-7),(5,10),(-10,-2),(3,4),(7,7),(8,-8),(-7,5),(-5,0),(-8,-5),(-4,-3),(-5,3),(3,3),(-2,0),(-5,-6),(6,4)]
# Setul de centre de Drone selectate din SP
#R = [(4,5),(6,6),(-7,-4),(-6,-3),(6,-5),(-3,4)]

# k = [1,2]
#Pk = {8: "Tip1", 12: "Tip2"}


def OP(I, R, Raza, k, Pk, priceSmall, priceBig):

    print("(Centrele de Drone Initial)R = ", R)
    # Coordonatele Centrelor de Drona Initiale
    xCentruDronaInainteEliminare = [i[0] for i in R]
    yCentruDronaInainteEliminare = [i[1] for i in R]

    # Ri = Fiecare set de drone cu fiecare pacient
    Ri = ParteaSP.CentrePacient(I, R, Raza)
    print("Ri = ", Ri)

    R1 = R
    R1, Ri = ParteaSP.SP(R, Ri)  # returneaza centrele de drona folosite
    # R1 = Centrele de Drone ramase dupa eliminare
    print("(Centrele de Drona dupa Eliminare)R1 =", R1)

    V = R1 + I
    # V = Centrele de drone care le folosim cu Pacientii care trebuie sa ii servim
    print('V = ', V)

    # CP = dictionar cu toate Centrele de Drone si Pacientii lor pe care ii poate accesa
    CP = ParteaSP.Centru_Pacienti(R1, Ri, I)
    print("CP = ", CP)
    # Dictionar puncte si numele lor
    IdPuncte = dict()

    fig, ax = plt.subplots()
    # Desenul Razei Centrele de Drone Initiale, Cu negru
    for i in R:
        a_circle = plt.Circle(i, Raza, color='k', linewidth=0.5, fill=False)
        cercuri = ax.add_artist(a_circle)
    # pune Centrele de Drone Inainte de Eliminare pe axa
    desenCoordonateCentruDrone1 = plt.scatter(
        xCentruDronaInainteEliminare, yCentruDronaInainteEliminare, c='k', marker='s')

    # Coordonatele Centrele de Drona Dupa Eliminare
    xCentruDronaDupaEliminare = [i[0] for i in R1]
    yCentruDronaDupaEliminare = [i[1] for i in R1]
    # Desenul Razei Centrele de Drone dupa Eliminare Centrelor Redundante, Cu Rosu
    for i in R1:
        a_circle = plt.Circle(i, Raza, color='r', linewidth=0.5, fill=False)
        ax.add_artist(a_circle)
    # pune Centrele de Drone Dupa Eliminare pe axa
    desenCoordonateCentruDrone2 = plt.scatter(
        xCentruDronaDupaEliminare, yCentruDronaDupaEliminare, c='r', marker='s')

    # setarea Raza Centrului de Drona sa incapa complet in imagine
    xlimMin = min(xCentruDronaDupaEliminare) - (Raza + 1)
    xlimMax = max(xCentruDronaDupaEliminare) + (Raza + 1)
    print("Maxim xCentruDrona = %d, Minim xCentruDrona = %d " %
          (xlimMax,  xlimMin))

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

    # Constangere pentru arcele dintre pacienti
    # A = Arcele de la pacientul i la pacientul j cu conditia sa fie in acelasi zona de acoeperire a Centrului de Drona
    A = [(V[i], V[j])for i in range(0, len(V)) for j in range(0, len(V)) for z in CP.keys() if i != j and (V[i] in CP[z] or V[i] in CP.keys())
         and (V[j] in CP[z] or V[j] in CP.keys()) and not(i < len(R1) and j < len(R1))]
    print("A = ", A)

    # Constangere pentru distanta dintre pacienti
    # Distanta de la pacientul i la pacientul j cu conditia sa fie in acelasi zona de acoperire a Centrului de Drona
    D = {(i, j): np.hypot(i[0]-j[0], i[1]-j[1]) for i, j in A}
    print("Distanta:", D)

    # Cantitatile de Livrare si de Preluare
    Pi = {i: rnd.randint(1, Pk[1]) for i in I}
    Pi.update({i: 0 for i in R1})
    # print(Pi) #Pick-up amount
    Di = {i: rnd.randint(1, Pk[1]) for i in I}
    Di.update({i: 0 for i in R1})
    # print(Di) #Delivery amount

    # Adaugam pe desen: Di = cantitatea de livrare & Pi = cantitatea de preluare
    # n = 0
    # for xy in zip(xPacient, yPacient):
    #     plt.annotate("Pi=(%d)Di=(%d)" % (Pi[I[n]], Di[I[n]]), xy=xy, textcoords='data')
    #     n += 1

    ProgresIncarcatura = {
        (i, j): (Pi[i] - Di[i] + Pi[j] - Di[j]) for i, j in A}
    print('PIncarcatura:', ProgresIncarcatura)

    mdl = Model('MIP Model')  # Mixed-Integer Programming

    # Denumim distanta de la pacientul i la pacientul j

    # hk = Cantitatea Arcului
    hk = mdl.binary_var_dict(A, name='Arc')
    u = mdl.continuous_var_dict(I, ub=Pk[1], name='DistantaParcurgere')
    Cantitate = mdl.continuous_var_dict(I, ub=Pk[1], name='CostMaximCantitate')
    print("Arcele + Denumirea:", hk)
    print("DistantaParcurgere + Denumirea:", u)
    print("CostMaximRidicare", Cantitate)
    # minimalizarea Zop (3) = Minimalizarea sumei costului de operare a dronei. Minimalizarea numarului de drone
    mdl.minimize(mdl.sum(D[i, j]*hk[i, j]for i, j in A))
    # Constrangere(4) = Asigura ca fiecare pacient este servit o singura data pentru i
    mdl.add_constraints(
        mdl.sum(hk[i, j] for i in V if j != i and (i, j) in hk.keys()) == 1 for j in I)
    # Constrangere(5) = Asigura ca fiecare pacient este servit o singura data pentru j
    mdl.add_constraints(
        mdl.sum(hk[i, j] for j in V if j != i and (i, j) in hk.keys()) == 1 for i in I)
    # Constangere(6) = Verifica ca drona sa nu viziteze acelasi element
    mdl.add_indicator_constraints(mdl.indicator_constraint(hk[i, j], u[i] + D[(i, j)] == u[j])for z in CP.keys()
                                  for i, j in A if i not in R1 and j not in R1)
    # Constrangere Cantitate
    mdl.add_indicator_constraints(mdl.indicator_constraint(hk[i, j], Cantitate[i] + ProgresIncarcatura[(i, j)] == Cantitate[j])
                                  for z in CP.keys() for i, j in A if i not in R1 and j not in R1)
    # Constrangere ce verifica distanta de zbor a dronei sa nu depaseasca distanta maxima(Drona Mare)
    mdl.add_constraints(u[i] >= D[(i, j)]
                        for i, j in A if i in u.keys() and j in u.keys())
    # Constrangere Cantitate
    mdl.add_constraints(Cantitate[i] >= ProgresIncarcatura[(
        i, j)] for i, j in A if i in Cantitate.keys() and j in Cantitate.keys())
    solution = mdl.solve(log_output=True)
    print(solution)

    active_arcs = [a for a in A if hk[a].solution_value > 0.9]
    print("Arcile active: ", active_arcs)
    desenArceActive = plt.scatter([i[0] for i in I], [i[1] for i in I], c='b')
    # Parcurgere fiecare pacient a fiecarei centru de drone si le pune in ordine in functie de arcele active
    # care le are
    directie = dict()
    for i, j in active_arcs:
        directie[i] = []
        directie[j] = []
    print("Dictionar cu directii goale ", directie)
    # Afisarea centrelor de drona pacientii lui,
    for i, j in active_arcs:
        directie[i].append(j)
    print("Dictionar cu directii la pacienti", directie)

    # caile care trebuie sa fie parcurse de la un centru de drona pana ajunge la alt centru de drona
    cai = []
    n = 0
    for i in directie.keys():
        if i in R:
            elemente = copy.deepcopy(directie[i])
            a = i
            while elemente != []:
                cai.append([])
                # adauga fiecare pacient la calea pe care o parcurgem
                cai[n].append(i)
                # valoarea dictionarului la cheia i
                j = elemente[0]
                # stergem elementul ca nu se repete
                del(elemente[0])
                while j not in R1:
                    # afiseaza pacientii in ordine in care sunt
                    cai[n].append(j)
                    a = j
                    j = directie[a][0]
                # afiseaza centru de drona de la care a pornit
                cai[n].append(j)
                n += 1
                print("Caile formate de la Centru de drone la Pacienti si inapoi", cai)

    # clasificare cai in functie de distanta lor, pentru a aplica Drona de Tip1 sau Drona de Tip2
    ClasificareCai = []
    nrBig = 0
    nrSmall = 0
    for i in cai:
        ClasificareCai.append([])
        sum = 0
        j = i[0]
        # Calcularea distanta de la centru de drone la pacienti si inapoi la centru de drone
        for z in i[1:]:
            sum += ParteaSP.distanta2Puncte(j, z)
            j = z
        print('Distanta cale', sum)
        ClasificareCai[-1].append(i)
        # clasificare in functie de Distanta daca este de Tip1 sau Tip2
        if sum <= Pk[0]:
            ClasificareCai[-1].append(0)
            print('Clasificare cai in functie de Distanta, Drona Mica', ClasificareCai)
        else:
            ClasificareCai[-1].append(1)
            print('Clasificare cai in functie de Distanta, Drona Mare', ClasificareCai)

    # Eliminam duplicatele
    unice = 0
    while unice == 0:
        unice = 1
        ClasificareCai2 = copy.deepcopy(ClasificareCai)
        for i in range(0, len(ClasificareCai)-1):
            for j in range(i+1, len(ClasificareCai)):
                if ClasificareCai[i] == ClasificareCai[j]:
                    del ClasificareCai2[j]
                    unice = 0
                    i = len(ClasificareCai)
                    ClasificareCai = ClasificareCai2
                    break
    # Drum la un singur centru
    ClasificareCai2 = copy.deepcopy(ClasificareCai)
    ElementeNoi = []
    for i in range(len(ClasificareCai)-1, -1, -1):
        if ClasificareCai[i][0][0] != ClasificareCai[i][0][-1]:
            'ClasificareCai[i][0][-1]=ClasificareCai[i][0][0]'
            print('arata', ClasificareCai[i][0][-1], ClasificareCai[i][0][0])
            L1 = ClasificareCai[i][0][:len(ClasificareCai[i][0])//2]
            L2 = ClasificareCai[i][0][len(ClasificareCai[i][0])//2:]
            print('L:', L1, L2)
            L1.append(L1[0])
            L2.insert(0, L2[-1])
            ElementeNoi.append([L1, 0])
            ElementeNoi.append([L2, 0])
            del ClasificareCai2[i]
    ClasificareCai = ClasificareCai2+ElementeNoi
    print('Elemente noi = ', ElementeNoi)
    print('ClasPct', ClasificareCai)

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
        elif c == 1:
            # deseneaza calea pentru drona de tip2
            nrBig += 1
            for z in range(0, len(j)-1):
                #plt.plot([j[z][0],j[z+1][0]],[j[z][1],j[z+1][1]],c = 'y', alpha = 0.6)
                plt.annotate('', xy=(j[z + 1][0], j[z + 1][1]), xycoords='data',
                             xytext=(j[z][0], j[z][1]), textcoords='data',
                             arrowprops=dict(frac=0.1, headwidth=5., width=0.5, color="y"))
    # Salveaza desenul
    plt.savefig(os.path.join('.', 'desen.png'), bbox_inches='tight')
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

    plt.savefig(os.path.join('.', 'desen2.png'), bbox_inches='tight')
    # ==
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
        DistantaPath = DistantaCale(i[0])

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
    return Pi, Di, DateTabel, PretCentru, TipDroneCentru, DistantaTotala, NrDroneMici, NrDroneMari, PretTotal, IdPuncte, len(I)


# Partea Euristica

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
        for i in permutare:
            Cale(Cai, Centre[i[0]], DistantaIncrc, PuncteInCentru, Pi, Di, I)


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


def Euristic(I, R, Raza, k, Pk, costLow, costBig, Pi, Di):
    Ri = ParteaSP.CentrePacient(I, R, Raza)
    R1, Ri = ParteaSP.SP(R, Ri)
    print(R1)
    xCentruDronaInainteEliminare = [i[0] for i in R]
    yCentruDronaInainteEliminare = [i[1] for i in R]
    print(Pi, Di)
    PuncteInCentru = dict()
    for i in R1:
        PuncteInCentru[i] = []
        for j in I:
            d = ParteaSP.distanta2Puncte(i, j)
            if(d <= Raza):
                PuncteInCentru[i].append((j, d))
        PuncteInCentru[i] = sorted(PuncteInCentru[i], key=lambda x: x[1])
    print(PuncteInCentru)

    IdPuncte = dict()

    fig, ax = plt.subplots()
    # Desenul Razei Centrele de Drone Initiale, Cu negru
    for i in R:
        a_circle = plt.Circle(i, Raza, color='k', linewidth=0.5, fill=False)
        cercuri = ax.add_artist(a_circle)
    # pune Centrele de Drone Inainte de Eliminare pe axa
    desenCoordonateCentruDrone1 = plt.scatter(
        xCentruDronaInainteEliminare, yCentruDronaInainteEliminare, c='k', marker='s')
    # desenCoordonateCentruDrone1.remove()

    # Coordonatele Centrele de Drona Dupa Eliminare
    xCentruDronaDupaEliminare = [i[0] for i in R1]
    yCentruDronaDupaEliminare = [i[1] for i in R1]
    # Desenul Razei Centrele de Drone dupa Eliminare Centrelor Redundante, Cu Rosu
    for i in R1:
        a_circle = plt.Circle(i, Raza, color='r', linewidth=0.5, fill=False)
        ax.add_artist(a_circle)
    # pune Centrele de Drone Dupa Eliminare pe axa
    desenCoordonateCentruDrone2 = plt.scatter(
        xCentruDronaDupaEliminare, yCentruDronaDupaEliminare, c='r', marker='s')

    # setarea Raza Centrului de Drona sa incapa complet in imagine
    xlimMin = min(xCentruDronaDupaEliminare) - (Raza + 1)
    xlimMax = max(xCentruDronaDupaEliminare) + (Raza + 1)
    print("Maxim xCentruDrona = %d, Minim xCentruDrona = %d " %
          (xlimMax,  xlimMin))

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

    permutari = list(itertools.permutations([i]for i in range(0, len(R1))))
    I2 = copy.deepcopy(I)
    Cai = []
    Cai2 = []
    n = 0
    nrSmall = 0
    nrBig = 0
    Cai = Optimizare(permutari, Cai, Pk, PuncteInCentru, Pi, Di, I, R1)

    for i in Cai:
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
        elif c == 1:
            # deseneaza calea pentru drona de tip2
            nrBig += 1
            for z in range(0, len(j)-1):
                #plt.plot([j[z][0],j[z+1][0]],[j[z][1],j[z+1][1]],c = 'y', alpha = 0.6)
                plt.annotate('', xy=(j[z + 1][0], j[z + 1][1]), xycoords='data',
                             xytext=(j[z][0], j[z][1]), textcoords='data',
                             arrowprops=dict(frac=0.1, headwidth=5., width=0.5, color="y"))

    plt.savefig(os.path.join('.', 'Euristic.png'), bbox_inches='tight')

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
    for i in Cai:
        j = i[0]
        c = i[1]
        if c == 0:
            # deseneaza calea pentru drona de Tip 1
            for z in range(0, len(j) - 1):
                # plt.plot([j[z][0],j[z+1][0]],[j[z][1],j[z+1][1]],c = 'g', alpha = 0.6)
                plt.annotate('', xy=(j[z + 1][0], j[z + 1][1]), xycoords='data',
                             xytext=(j[z][0], j[z][1]), textcoords='data',
                             arrowprops=dict(frac=0.1, headwidth=5., width=0.5, color="g"))
        elif c == 1:
            # deseneaza calea pentru drona de tip2
            for z in range(0, len(j) - 1):
                # plt.plot([j[z][0],j[z+1][0]],[j[z][1],j[z+1][1]],c = 'y', alpha = 0.6)
                plt.annotate('', xy=(j[z + 1][0], j[z + 1][1]), xycoords='data',
                             xytext=(j[z][0], j[z][1]), textcoords='data',
                             arrowprops=dict(frac=0.1, headwidth=5., width=0.5, color="y"))

    plt.savefig(os.path.join('.', 'Euristic2.png'), bbox_inches='tight')
    DateTabel = dict()
    PretCentru = dict()
    TipDroneCentru = dict()
    for i in Cai:
        DateTabel[IdPuncte[i[0][0]]] = []
        PretCentru[IdPuncte[i[0][0]]] = 0
        TipDroneCentru[IdPuncte[i[0][0]]] = [0, 0]
    NrDroneMici = 0
    NrDroneMari = 0
    DistantaTotala = 0
    PretTotal = 0

    for i in Cai:
        if i[1] == 0:
            NrDroneMici += 1
            TipDroneCentru[IdPuncte[i[0][0]]][0] += 1
            PretCentru[IdPuncte[i[0][0]]] += costLow
            PretTotal += costLow
        else:
            NrDroneMari += 1
            TipDroneCentru[IdPuncte[i[0][0]]][1] += 1
            PretCentru[IdPuncte[i[0][0]]] += costBig
            PretTotal += costBig
        DistantaPath = DistantaCale(i[0])

        DateTabel[IdPuncte[i[0][0]]].append([i[0], DistantaPath])

        DistantaTotala += DistantaPath

    for i in DateTabel.keys():
        for z in range(0, len(DateTabel[i])):
            for j in range(0, len(DateTabel[i][z][0])):
                DateTabel[i][z][0][j] = IdPuncte[DateTabel[i][z][0][j]]
            DateTabel[i][z][1] = round(DateTabel[i][z][1], 2)

    print('D=', DateTabel)
    print(DistantaTotala, NrDroneMici, NrDroneMari, PretTotal)
    print(PretCentru)
    print(TipDroneCentru)
    return DateTabel, PretCentru, TipDroneCentru, DistantaTotala, NrDroneMici, NrDroneMari, PretTotal, IdPuncte, len(I)


def Cost(a, b):
    return math.sqrt(pow(a[0][1] - b[0][1], 2) + pow(a[0][0] - b[0][0], 2))+a[1] - a[2] + b[1] - b[2]

def Eliminare(path1,path2):
    n1=copy.deepcopy(path1)
    n2=copy.deepcopy(path2)
    for i in path1:
        if i in path2:
            aux1=copy.deepcopy(n1)
            aux2=copy.deepcopy(n2)
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
            if DistantaCale(Puncte1)+s1<=DistantaCale(Puncte2)+s2:
                n2= aux2
            else:
                n1 = aux1
    path1=n1
    path2=n2
    return path1,path2

def ImpartireInCai(tur,limita,centru,Pi,Di):
    Cai = [[]]
    n=0
    cale = []
    i = 0
    while i !=len(tur):
        cale2=copy.deepcopy(cale)
        cale2.append(tur[i])
        s=0
        for j in cale2:
            s+= Pi[j]-Di[j]
        if ParteaSP.distanta2Puncte(centru, cale2[0]) + DistantaCale(cale2) + ParteaSP.distanta2Puncte(centru, cale2[-1]) <= limita and abs(s)<= limita:

            cale = cale2
            Cai[n] = cale
            i+=1

        else:
            if Cai[n] == []:
                print('cale----',centru,cale2,ParteaSP.distanta2Puncte(centru, cale2[0]) + DistantaCale(cale2) + ParteaSP.distanta2Puncte(centru, cale2[-1]),cale)
                break
            cale = []
            Cai.append([])
            n+=1

        #print(Cai)
        #print(tur)
    return Cai



def MiniAco(nodes):
    world = pants.World(nodes, Cost)

    solver = pants.Solver()
    solution = solver.solve(world)
    # or
    solutions = solver.solutions(world)

    #print('distance',solution.distance)
    #print('tour',solution.tour)    # Nodes visited in order
    #print('path',solution.path)    # Edges taken in order
    # or
    best = float("inf")
    bestT = 0
    for solution in solutions:
        assert solution.distance < best
        best = solution.distance
        bestT = solution.tour
    #bestT.insert(0,centru)
    #bestT.append(centru)
    return bestT


def ACO(I, R, Raza, k, Pk, priceSmall, priceBig,Pi,Di):
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
    bestCai=[]
    for i in PuncteInCentru:
        for j in range(0,len(PuncteInCentru[i])):
            PuncteInCentru[i][j]=(PuncteInCentru[i][j][0],Pi[PuncteInCentru[i][j][0]],Di[PuncteInCentru[i][j][0]])
        print('Puncte',PuncteInCentru[i])
        bestCai.append(MiniAco(PuncteInCentru[i]))
    print(PuncteInCentru)
    print('bestCai1',bestCai)
    for i in range(0,len(bestCai)-1):
        for j in range(i+1,len(bestCai)):
            bestCai[i],bestCai[j]=Eliminare(bestCai[i],bestCai[j])
    for i in range(0,len(bestCai)):
        for j in range(0,len(bestCai[i])):
            bestCai[i][j] = bestCai[i][j][0]
    print('Best',bestCai)

    CaiFinale = []
    for i in range(0,len(R1)):
        Lista = ImpartireInCai(bestCai[i], Pk[1], R1[i], Pi, Di)
        for j in range(0,len(Lista)):
            Lista[j].insert(0,R1[i])
            Lista[j].append(R1[i])
            CaiFinale.append(Lista[j])
    print('CaiFinale',CaiFinale)
    for i in CaiFinale:
        d = DistantaCale(i)
        print('D=',d)

    ClasificareCai = []
    nrBig = 0
    nrSmall = 0
    for i in CaiFinale:
        d=DistantaCale(i)
        s=0
        for j in i:
            s += Pi[j] - Di[j]
        if d>Pk[0] or abs(s)>Pk[0]:
            ClasificareCai.append([i,1])
            nrBig+=1
        else:
            ClasificareCai.append([i, 0])
            nrSmall+=1

    print('Clasif',ClasificareCai)

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
    print("Maxim xCentruDrona = %d, Minim xCentruDrona = %d " % (xlimMax, xlimMin))

    ylimMin = min(yCentruDronaDupaEliminare) - (Raza + 1)
    ylimMax = max(yCentruDronaDupaEliminare) + (Raza + 1)
    print("Maxim yCentruDrona = %d, Minim yCentruDrona = %d " % (ylimMax, ylimMin))
    # Construirea Dimensiunei Imaginei
    ax.set(xlim=(xlimMin, xlimMax), ylim=(ylimMin, ylimMax))

    # Pacientii
    xPacient = [i[0] for i in I]
    yPacient = [i[1] for i in I]
    desenCoordonatePacienti = plt.scatter(xPacient, yPacient, c='b')  # pune pacientii pe axa
    # numerotam pacientii
    n = 1
    for xy in zip(xPacient, yPacient):
        plt.annotate("p%d" % (n), xy=xy, textcoords='data')
        IdPuncte[xy] = "p%d" % (n)
        n += 1

    # Numerotam Centrele de Drona Inainte Eliminare
    n = 1
    for xy in zip(xCentruDronaInainteEliminare, yCentruDronaInainteEliminare):
        numerotareCentreDrona = plt.annotate("D%d" % (n), xy=xy, textcoords='data')
        IdPuncte[xy] = "D%d" % (n)
        n += 1
    print("Id=", IdPuncte)

    for i in ClasificareCai:
        j = i[0]
        c = i[1]
        if c == 0:
    #deseneaza calea pentru drona de Tip 1
            nrSmall += 1
            for z in range(0, len(j)-1):
                #plt.plot([j[z][0],j[z+1][0]],[j[z][1],j[z+1][1]],c = 'g', alpha = 0.6)
                plt.annotate('', xy=(j[z+1][0], j[z+1][1]), xycoords='data',
                             xytext=(j[z][0], j[z][1]), textcoords='data',
                             arrowprops=dict(frac=0.1, headwidth=5., width=0.5, color ="g"))
                # print("j[z][0]=", j[z][0], "j[z][1]", j[z][1], "j[z+1][0]", j[z+1][0], "j[z+1][1]", j[z+1][1])
                # print(j[z], j[z+1], j)
        elif c == 1:
        # deseneaza calea pentru drona de tip2
            nrBig += 1
            for z in range(0,len(j)-1):
                #plt.plot([j[z][0],j[z+1][0]],[j[z][1],j[z+1][1]],c = 'y', alpha = 0.6)
                plt.annotate('', xy=(j[z + 1][0], j[z + 1][1]), xycoords='data',
                             xytext=(j[z][0], j[z][1]), textcoords='data',
                             arrowprops=dict(frac=0.1, headwidth=5., width=0.5, color="y"))
    #Salveaza desenul
    plt.savefig(os.path.join('.', 'ant1.png'), bbox_inches='tight')
    plt.close()

    fig, ax = plt.subplots()
    print('R1=',R1)
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
            numerotareCentreDrona = plt.annotate("D%d" % (n), xy=xy, textcoords='data')
        n += 1
    #==
    for i in ClasificareCai:
        j = i[0]
        c = i[1]
        if c == 0:
    #deseneaza calea pentru drona de Tip 1
            for z in range(0, len(j)-1):
                #plt.plot([j[z][0],j[z+1][0]],[j[z][1],j[z+1][1]],c = 'g', alpha = 0.6)
                plt.annotate('', xy=(j[z+1][0], j[z+1][1]), xycoords='data',
                             xytext=(j[z][0], j[z][1]), textcoords='data',
                             arrowprops=dict(frac=0.1, headwidth=5., width=0.5, color ="g"))
                # print("j[z][0]=", j[z][0], "j[z][1]", j[z][1], "j[z+1][0]", j[z+1][0], "j[z+1][1]", j[z+1][1])
                # print(j[z], j[z+1], j)
        elif c == 1:
        # deseneaza calea pentru drona de tip2
            for z in range(0,len(j)-1):
                #plt.plot([j[z][0],j[z+1][0]],[j[z][1],j[z+1][1]],c = 'y', alpha = 0.6)
                plt.annotate('', xy=(j[z + 1][0], j[z + 1][1]), xycoords='data',
                             xytext=(j[z][0], j[z][1]), textcoords='data',
                             arrowprops=dict(frac=0.1, headwidth=5., width=0.5, color="y"))

    plt.savefig(os.path.join('.', 'ant2.png'), bbox_inches='tight')
    #plt.show()
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
        DistantaPath = DistantaCale(i[0])

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

def Tabel(grid, DateTabel, PretCentru, TipDroneCentru, DistantaTotala, NrDroneMici, NrDroneMari, PretTotal, IdPuncte, nrPacienti, timp, Pi, Di):

    p=0
    for i in IdPuncte:
        if IdPuncte[i].find('D') != 0:
            p+=1
    grid.CreateGrid(len(PretCentru)+4+p, 7)

    # We can set the sizes of individual rows and columns
    # in pixels
    grid.SetRowSize(0, 60)
    grid.SetColSize(0, 120)
    grid.SetColSize(1, 120)
    grid.SetColSize(2, 120)
    grid.SetColSize(4, 200)

    # We can specify the some cells will store numeric
    # values rather than strings. Here we set grid column 5
    # to hold floating point values displayed with width of 6
    # and precision of 2
    #grid.SetColFormatFloat(5, 6, 2)

    grid.SetCellValue(0, 0, 'Centru de Drone')
    grid.SetCellValue(0, 1, 'Pacienti')
    grid.SetCellValue(0, 2, 'Numar de drone')
    grid.SetCellValue(0, 3, 'Cost($)')
    grid.SetCellValue(0, 4, 'Traseele si distanta parcursa de ele')
    grid.SetCellValue(0, 5, 'Suma Distantelor parcurse')
    grid.SetCellValue(0, 6, 'Timpul de executie')
    grid.SetCellValue(len(PretCentru)+1, 0, 'Nr Centre: %d' % len(PretCentru))
    grid.SetCellValue(len(PretCentru)+1, 1, str(nrPacienti)+' Pacienti')
    grid.SetCellValue(len(PretCentru)+1, 2, ' %d (Tip I: %d Tip II: %d)' %
                      (NrDroneMici+NrDroneMari, NrDroneMici, NrDroneMari))
    grid.SetCellValue(len(PretCentru)+1, 3, str(PretTotal)+'$')
    grid.SetCellValue(len(PretCentru)+1, 5, str(round(DistantaTotala, 2)))
    grid.SetCellValue(len(PretCentru)+1, 6, str(round(timp, 2))+' ms')
    PacientiCentru = dict()
    for i in DateTabel.keys():
        PacientiCentru[i] = set()
    for i in DateTabel.keys():
        for z in range(0, len(DateTabel[i])):
            for j in range(0, len(DateTabel[i][z][0])):
                if DateTabel[i][z][0][j][0] != 'D':
                    PacientiCentru[i].add(DateTabel[i][z][0][j])
    print(PacientiCentru)
    n = 1
    for i in DateTabel.keys():
        grid.SetCellValue(n, 0, str(i))
        for j in PacientiCentru[i]:
            grid.SetCellValue(n, 1, grid.GetCellValue(n, 1)+str(j)+' ')
        grid.SetCellValue(n, 2, 'Tip I:%d Tip II:%d' %
                          (TipDroneCentru[i][0], TipDroneCentru[i][1]))
        grid.SetCellValue(n, 3, str(PretCentru[i])+'$')
        for j in DateTabel[i]:
            for z in j[0]:
                grid.SetCellValue(n, 4, grid.GetCellValue(n, 4)+str(z)+' ')
            grid.SetCellValue(n, 4, grid.GetCellValue(
                n, 4) + str(j[1]) + ' | ')
        n += 1

    grid.SetCellValue(len(PretCentru) + 3, 0,'Pacienti cu Cantitatea de ridicare si primire')
    grid.SetCellValue(len(PretCentru) + 3, 1, 'Ridicare')
    grid.SetCellValue(len(PretCentru) + 3, 2, 'Livrare')


    m=0
    for i in IdPuncte:
        if IdPuncte[i].find('D') != 0:
            grid.SetCellValue(len(PretCentru) + 4+m, 0, str(IdPuncte[i]))
            grid.SetCellValue(len(PretCentru) + 4 + m, 1, str(Pi[i]))
            grid.SetCellValue(len(PretCentru) + 4 + m, 2, str(Di[i]))
            m+=1


