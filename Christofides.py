# -*- coding: utf-8 -*-
"""
ALGORITMO DE CHRISTOPIDES

1. Obtener un árbol de recubrimiento mínimo,T
2. Determinar el conjunto de vértices,O, que tienen grado impar
3. Determinar un apareamiento perfecto, M, de peso mínimo del grafo completo con los vértices de O
4. Combinar las aristas de T y M para obtener un multigrafo
5. Obtener un ciclo euleriano, H.
6. Obtener un ciclo hamiltoniano a partir del euleriano anterior
"""

import math
import random

"""
Construyo el grafo con los datos dados, se contruye con listas de adyacencia.
Definimos un diccionario vacío y cada clave es un vértice y cuya lista asociada
son pares, vértice, distancia.
"""

datos = [[1.0,565.0,575.0],[2.0,25.0,185.0],[3.0,345.0,750.0],[4.0,945.0,685.0],[5.0,845.0,655.0],
      [6.0,880.0,660.0],[7.0,25.0,230.0],[8.0,525.0,1000.0],[9.0,580.0,1175.0],[10.0,650.0,1130.0],
      [11.0,1605.0,620.0],[12.0,1220.0,580.0],[13.0,1465.0,200.0],[14.0,1530.0,5.0],[15.0,845.0,680.0],
      [16.0,725.0,370.0],[17.0,145.0,665.0],[18.0,415.0,635.0],[19.0,510.0,875.0],[20.0,560.0,365.0],
      [21.0,300.0,465.0],[22.0,520.0,585.0],[23.0,480.0,415.0],[24.0,835.0,625.0],[25.0,975.0,580.0],
      [26.0,1215.0,245.0],[27.0,1320.0,315.0],[28.0,1250.0,400.0],[29.0,660.0,180.0],[30.0,410.0,250.0],
      [31.0,420.0,555.0],[32.0,575.0,665.0],[33.0,1150.0,1160.0],[34.0,700.0,580.0],[35.0,685.0,595.0],
      [36.0,685.0,610.0],[37.0,770.0,610.0],[38.0,795.0,645.0],[39.0,720.0,635.0],[40.0,760.0,650.0],
      [41.0,475.0,960.0],[42.0,95.0,260.0],[43.0,875.0,920.0],[44.0,700.0,500.0],[45.0,555.0,815.0],
      [46.0,830.0,485.0],[47.0,1170.0,65.0],[48.0,830.0,610.0],[49.0,605.0,625.0],[50.0,595.0,360.0],
      [51.0,1340.0,725.0],[52.0,1740.0,245.0]]


def principal():
    G,G2 = construir_grafo(datos)
    n = len(datos)
    
    # Obtener un árbol mínimo
    Aminimo = arbol_minimo(G,n)
    
    #Determinar los vértices de grado impar en Aminimo
    vertices_impares = vertices_impar(Aminimo)
    #Apareamiento perfecto minimo y combinacio con Aminimo
    apareamiento_perfecto_minimo(Aminimo, G2, vertices_impares)
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
            if v != u and grafo[v][u] < longitud:
                longitud = grafo[v][u]
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