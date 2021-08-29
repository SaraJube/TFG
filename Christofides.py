# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 20:20:36 2021

@author: Sara
"""
import math
import random
import extraccion_datos

dic,m1,datos = extraccion_datos.principal('./datos/a280_datos.txt')

def principal():
    G,G2 = construir_grafo(m1)
    print(G)
    n = len(m1)
    
    # Obtener un árbol mínimo
    Aminimo = arbol_minimo(G,n)
    
    #Determinar los vértices de grado impar en Aminimo
    vertices_impares = vertices_impar(Aminimo)
    #Apareamiento perfecto minimo y combinacio con Aminimo
    apareamiento_perfecto_minimo(Aminimo, datos, vertices_impares)
    #Obtener ciclo euleriano
    ciclo = ciclo_euleriano(Aminimo)
    
    #Obtener ciclo hamiltoniano
    actual = ciclo[0]
    camino = [actual]
    visitado = [False]*(len(ciclo)+1)
    visitado[0] = True
    visitado[1] = True
    longitud = 0
    for v in ciclo[1:]:
        if not visitado[v]:
            camino.append(v)
            visitado[v] = True
            longitud += G2[actual][v]
            actual = v
    return longitud,camino
  
def construir_grafo(datos):
    grafo = {}
    grafo2 = {}
    for i in range(len(datos)):
        for j in range(len(datos)):
            if i != j:
                a = int(datos[i][0])
                if a not in grafo:
                    grafo[a] = []
                    grafo2[a] = {}
                dis = obtener_distancia(datos,i,j)
                grafo[a].append((int(datos[j][0]),dis))
                grafo2[a][int(datos[j][0])] = dis
    return grafo,grafo2

def obtener_distancia(datos,i,j):
    a1 = abs(datos[i][1]-datos[j][1])
    a2 = abs(datos[i][2]-datos[j][2])
    dis = math.sqrt(a1**2+a2**2)
    return dis

# El árbol mínimo será una lista de pares, aristas (se representa como un par de vértices)
def arbol_minimo(grafo,n): #Prim
    ARM = []
    M = Monticulo_pares(n)
    coste_min = crear_coste(n)
    conexion = crear_conexion(n)
    l = copiar(grafo[1])
    while l != []:
        i = l[0][0]
        coste_min[i] = l[0][1]
        M.añadir(i,coste_min[i])
        l.pop(0)
    for _ in range(n-1):
        minimo = M.minimo()
        M.eliminar_minimo()
        elegido = minimo[0]
        a = (elegido,conexion[elegido])
        ARM.append(a)
        coste_min[elegido] = -1
        l = copiar(grafo[elegido])
        while l != []:
            w = l[0][0]
            if l[0][1] < coste_min[w]:
                coste_min[w] = l[0][1]
                conexion[w] = elegido
                M.modificar(w, coste_min[w])
            l.pop(0)
    return ARM

def copiar(lista):
    l = []
    for i in range(len(lista)):
        l.append(lista[i])
    return l

def crear_coste(n):
    l = [-1,-1]
    for i in range(2,n+1):
        l.append(float("inf"))
    return l

def crear_conexion(n):
    l = []
    for _ in range(n+1):
        l.append(1)
    return l

class Monticulo_pares():

    def __init__(self,n):
        self.lista = [(0,float("inf"))]
        self.ultimo = 0
        self.posiciones = self.lista_posi(n)
        
    def lista_posi(self,n):
        l = [0]
        for _ in range(n):
            l = l+[-1]
        return l

    def añadir(self,elem,prio):
        if self.posiciones[elem] != -1:
            pass
        else:
            self.ultimo = self.ultimo + 1
            self.lista = self.lista+[(elem,prio)]
            self.posiciones[elem] = self.ultimo
            self.flotar_pares(self.ultimo)

    def flotar_pares(self,j):
        i = j
        while i != 1 and self.lista[i][1] < self.lista[i//2][1]:
            self.intercambiar(i,i//2)
            i = i // 2
    
    def intercambiar(self,i,j):
        aux = self.lista[i]
        self.lista[i]=self.lista[j]
        self.lista[j] = aux
        self.posiciones[self.lista[i][0]] = i
        self.posiciones[self.lista[j][0]] = j
    
    def modificar(self,elem, prio):
        i = self.posiciones[elem]
        if i == -1:
            self.añadir(elem,prio)
        else:
            a = self.lista[i][0]
            self.lista[i] = (a,prio)
            if i != 1 and self.lista[i][1] < self.lista[i//2][1]:
                self.flotar_pares(i)
            else:
                self.hundir_pares(i)
    
    def minimo(self):
        return self.lista[1]
    
    def eliminar_minimo(self):
        self.posiciones[self.lista[1][0]] = -1
        self.lista[1] = self.lista[self.ultimo]
        self.posiciones[self.lista[1][0]] = 1
        self.ultimo = self.ultimo - 1
        self.lista.pop()
        self.hundir_pares(1)
        
    def hundir_pares(self,j):
        fin = False
        i = j
        k = self.ultimo
        while 2*i <= k and not fin:
            if 2*i+1 <=k and self.lista[2*i+1][1] < self.lista[2*i][1]:
                m =2*i+1
            else:
                m = 2*i
            if self.lista[m][1] < self.lista[i][1]:
                self.intercambiar(i,m)
                i = m
            else:
                fin = True

    def obtener_lista(self):
        return self.lista

def vertices_impar(ARM):
    grados = {}
    vertices = []
    for arista in ARM:
        if arista[0] not in grados:
            grados[arista[0]]=0
        if arista[1] not in grados:
            grados[arista[1]] = 0
        grados[arista[0]] += 1
        grados[arista[1]] += 1
    
    for vertice in grados:
        if grados[vertice] % 2 == 1:
            vertices.append(vertice)
    return vertices

def apareamiento_perfecto_minimo(ARM,grafo,v_impares):
    random.shuffle(v_impares) 
    while v_impares != []:
        v = v_impares.pop()
        longitud = float("inf")
        u = 1
        cercano = 0
        for u in v_impares:
            if v <= u:
                dis = grafo[v][u]
            else:
                dis = grafo[u][v]
            if v != u and dis < longitud:
                longitud = dis
                cercano = u
                
        ARM.append((v,cercano))
        v_impares.remove(cercano)
        
def ciclo_euleriano(AMR):
    vecinos = {}
    for arista in AMR:
        if arista[0] not in vecinos:
            vecinos[arista[0]] = []
        if arista[1] not in vecinos:
            vecinos[arista[1]] = []
        vecinos[arista[0]].append(arista[1])
        vecinos[arista[1]].append(arista[0])
    vertice_inicial = AMR[0][0]
    EP = [vecinos[vertice_inicial][0]]
    while len(AMR) > 0:
        for i,v in enumerate(EP):
            if len(vecinos[v]) > 0:
                break
            
        while len(vecinos[v]) > 0:
            w = vecinos[v][0]
            AMR = eliminar_arista(AMR,v,w)
            del vecinos[v][(vecinos[v].index(w))]
            del vecinos[w][(vecinos[w].index(v))]
            i += 1
            EP.insert(i,w)
            
            v = w
    return EP
            
def eliminar_arista(AMR,i,j):
    for k,item in enumerate(AMR):
        if (item[0]==i and item[1] == j) or (item[0]==j and item[1]== i):
            del AMR[k]
    return AMR

print(principal())
# f= open("berlin52_Christofides.txt",'w')
# for k in range(30):
#     f.write("Repetición: "+str(k+1)+"\n")
#     print("Repetición",k+1)
#     p = principal()
#     l = []
#     for i in p[1]:
#         l.append(i)
#     print(p)
#     f.write(str(l)+" "+str(p[0])+"\n")
# f.close()
