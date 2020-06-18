import math
import copy
# Pacienti = [(10,-5),(6,-3),(2,8),(9,-7),(5,10),(-10,-2),(3,4),(7,7),(8,-8),(-7,5),(-5,0),(-8,-5),(-4,-3),(-5,3),(3,3),(-2,0),(-5,-6),(6,4)]
# CentreDrona = [(4,5),(6,6),(-7,-4),(-6,-3),(6,-5),(-3,4)]


def inZona(pacient, centru, raza):
    return (math.sqrt(math.pow(pacient[0]-centru[0], 2)+math.pow(pacient[1]-centru[1], 2))) <= raza
# verifica daca un pacient dat se afla in raza zonei de centre de drone date
# print(inZona((10,-5),(6,6),6))


def distanta2Puncte(pacient, centru):
    return math.sqrt(math.pow(pacient[0]-centru[0], 2)+math.pow(pacient[1]-centru[1], 2))
# calculeaza distanta de la un pacient(I) dat la un centru de drona dat(R)
# print(distanta2Puncte((6,6),(4,5)))


def CentrePacient(pacienti, centredrona, raza):
    Ri = []
    for i in range(0, len(pacienti)):
        Ri.append([])
        for j in range(0, len(centredrona)):
            if(inZona(pacienti[i], centredrona[j], raza)):
                Ri[i].append(centredrona[j])
    return Ri
# verifica pentru fiecare pacient in ce raza carui centru de drone se afla
# se afiseaza o lista cu listele de coordonatele(Ri) ale fiecarui centru de drone care are pacientul,
# respectiv in raza lui
# Pentru fiecare nod am stabilit de care centru de drone a fost deservit
#Ri = CentrePacient(Pacienti,CentreDrona,Raza)


def Scoatere(centreDrone, Ri, Centru):
    c2 = copy.deepcopy(centreDrone)
    c2.remove(Centru)
    R2 = copy.deepcopy(Ri)
    for i in range(0, len(R2)):  # scoate centru de la fiecare pacient din centru
        try:
            R2[i].remove(Centru)
        except ValueError:
            pass
        if len(R2[i]) == 0:  # daca centru a fost scos si pacientul este in afara atunci nu se modifica,
            return centreDrone, Ri, False
    return c2, R2, True
# Scoate un centru de drona si verifica daca acel centru de drona afecteaza starea initiala a centrelor de drone
# a,b,c=(Scoatere(CentreDrona,CentrePacient(Pacienti,CentreDrona,Raza),(6,-5)))
#print(a,'\n',b ,'\n',c)


def SP(centredrona, Ri):
    popular = dict()
    for i in centredrona:
        popular[i] = 0
    for i in Ri:  # Ri lista de pacienti cu coordonatele centrelor de drona
        for j in i:  # j este un centru din i
            # pentru fiecare centru de drona gasit se adauga pacientul
            popular[j] += 1
    popular = sorted(popular.items(), key=lambda x: x[1], reverse=True)
    # Dictionar in care sortez centrele de drone descrescator dupa numarul de pacienti
    ok = 1
    while ok:
        ok = 0
        for i in range(0, len(popular)):
            centredrona, Ri, t = Scoatere(centredrona, Ri, popular[i][0])
            # scoate cele mai populare centre de drone
            if t == True:
                ok = 1
                # daca poate scoate cu succes un centru de drona, atunci se stege.
                popular.pop(i)
                break
    print(Ri)
    return centredrona, Ri
#Ri = CentrePacient(Pacienti,CentreDrona,Raza)
# CentreDrona,Ri=SP(CentreDrona,Ri,1) #returneaza centrele de drona folosite
# print(CentreDrona)

# Pregatit centrele pentru OP
# se ia toti pacientii comuni si creaza fiecare zona a centrelor de drona cu pacientii lor


def Centru_Pacienti(centredrone, Ri, Pacienti):
    # Un dictionar care are ca si chei centrele de drona si ca valoare o lista cu pacientii care au acel
    # centru cel mai apropiet de ei.
    centru_pacient = dict()
    for i in centredrone:
        centru_pacient[i] = []
    for i in range(0, len(Pacienti)):
        for j in Ri[i]:
            # adauga pacientul in centru de drona unde are distanta minima
            centru_pacient[j].append(Pacienti[i])
    return centru_pacient
