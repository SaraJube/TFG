# -*- coding: utf-8 -*-
"""
Empezando en el primer nodo
Berlin 52
ACS
([0, 24, 20, 19, 18, 2, 1, 41, 16, 9, 8, 39, 4, 5, 6, 7, 3, 10, 11, 12, 13, 14, 15, 17, 21, 22, 
  23, 25, 26, 27, 28, 29, 30, 32, 31, 33, 34, 35, 36, 37, 38, 40, 42, 43, 44, 45, 46, 47, 
  48, 49, 50], 19820.790981082362)
"""

import threading
import random
import math
m1 = [[1.0,565.0,575.0],[2.0,25.0,185.0],[3.0,345.0,750.0],[4.0,945.0,685.0],[5.0,845.0,655.0],
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

def matriz_distancias(datos):
    l = []
    for i in range(len(datos)):
        s = []
        for j in range(len(datos)):
            if not(i == j):
                a1 = abs(datos[i][1]-datos[j][1])
                a2 = abs(datos[i][2]-datos[j][2])
                dis = math.sqrt(a1**2+a2**2)
            else:
                dis = 0
            s.append(dis)
        l.append(s)
    return l
   
mapa_dis= matriz_distancias(m1)
alpha = 1
beta = 3
coef_disipacion = 0.03
feromona_inicial = 0.32985169
nhormigas= len(m1)
iteraciones= 1000
coef_local = 0.3

class Hormiguero():
    class Hormiga():
        
        def __init__(self,inicio,distancias, feromonas, alpha, beta):
            self.nodo_actual = inicio
            self.mapa_feromonas = feromonas
            self.mapa_distancias = distancias
            self.recorrido = [inicio]
            self.alpha = float(alpha)
            self.beta = float(beta)
            self.tamaño = len(distancias)
            self.distancia = 0.0
            self.completo = len(self.recorrido) == self.tamaño -1
            
        def run(self,mapa):
            siguiente = self.siguiente_destino(mapa)
            self.distancia += float(self.mapa_distancias[siguiente][self.nodo_actual])
            inicial = self.nodo_actual
            self.nodo_actual = siguiente
            self.recorrido.append(siguiente)
            self.distancia += float(self.mapa_distancias[self.nodo_actual][self.recorrido[0]])
            return (inicial, self.nodo_actual)

    
        def siguiente_destino(self,mapa):
            s = []
            total = 0.0
            a = self.nodo_actual
            for x in range(self.tamaño):
                if not (x==a) and  not(x in self.recorrido):
                    feromona = float(mapa[a][x])
                    dista = float(self.mapa_distancias[a][x])
                    proba = pow(feromona,self.alpha)*pow(1/dista,self.beta)
                    total += proba
                    s.append([x,proba])
            total = float(total)

            if total == 0.0:
                def next_up(x):
                    import struct
                    if math.isnan(x) or (math.isinf(x) and x > 0):
                        return x
                    if x == 0.0:
                        x = 0.0
                    n = struct.unpack('<q', struct.pack('<d', x))[0]
                    if n >= 0:
                        n += 1
                    else:
                        n -= 1
                    return struct.unpack('<d', struct.pack('<q', n))[0]

                for a in s:
                    a[1] = next_up(a[1])
                total = next_up(total)
                
            fin = True
            while fin:
                numero = random.random()
                acumulacion = 0.0
                for i in range(len(s)):
                    probabilidad = s[i][1]/float(total)
                    if numero <= probabilidad + acumulacion:
                        fin = False
                        return s[i][0]
                    acumulacion += s[i][1]


    
        def obtener_resultados(self):
            return self.distancia,self.recorrido
        
        def obtener_recorrido(self):
            if len(self.recorrido) == self.tamaño -1:
                return self.recorrido
            return []
        
        def obtener_distancia(self):
            if len(self.recorrido) == self.tamaño -1:
                return float(self.distancia)
            return 0.0
        
    
    def __init__(self,mapa_dis,feromona_inicial,alpha,beta,coef_disipacion,nhormigas,iteraciones):
        self.tamaño = len(mapa_dis)
        self.mapa_distancia = mapa_dis
        self.mapa_feromona = self.matriz_inicial(feromona_inicial)
        self.mapa_feromona_local = self.matriz_inicial(feromona_inicial)
        self.alpha = float(alpha)
        self.beta = float(beta)
        self.coef_disipacion = float(coef_disipacion)
        self.nhormigas = nhormigas
        self.distancia_mas_corta = float("inf")
        self.mejor_camino = []
        self.mapa_feromonas_hormigas = self.matriz_inicial(0.0)
        self.iteraciones = iteraciones
        self.hormigas = self.inicio_hormigas()
        

    def matriz_inicial(self,cte):
        l = []
        for x in range(self.tamaño):
            s = []
            for x in range(self.tamaño):
                s.append(cte)
            l.append(s)
        return l
    
    
    def actualizacion_feromona(self):
        for x in range(self.tamaño):
            for y in range(self.tamaño):
                self.mapa_feromona[x][y] = (1-self.coef_disipacion)*self.mapa_feromona[x][y]
                self.mapa_feromona[x][y] += self.mapa_feromonas_hormigas[x][y]
            
        
    def feromona_hormiga(self,ruta,distancia):
        for i in range(len(ruta)-2):
            nodo1 = ruta[i]
            nodo2 = ruta[i+1]
            valor_actual = float(self.mapa_feromonas_hormigas[nodo1][nodo2])
            incremento = 1/distancia
            self.mapa_feromonas_hormigas[nodo1][nodo2] = valor_actual + incremento
            self.mapa_feromonas_hormigas[nodo2][nodo1] = valor_actual + incremento
        nodo1 = ruta[len(ruta)-1]
        nodo2 = ruta[0]
        valor_actual = float(self.mapa_feromonas_hormigas[nodo1][nodo2])
        incremento = 1/distancia
        self.mapa_feromonas_hormigas[nodo1][nodo2] = valor_actual + incremento
        self.mapa_feromonas_hormigas[nodo2][nodo1] = valor_actual + incremento
    
    def inicio_hormigas(self):
        l = []
        for _ in range(self.nhormigas):
            hormiga = self.Hormiga(0, self.mapa_distancia, self.mapa_feromona,self.alpha, self.beta)
            l.append(hormiga)
        return l
    
    def actualizar_feromona_local(self,l):
        for arista in l:
            a = arista[0]
            b = arista[1]
            valor = self.mapa_feromona_local[a][b]
            self.mapa_feromona_local[a][b] = (1-coef_local)*valor+coef_local*feromona_inicial
            self.mapa_feromona_local[b][a] = (1-coef_local)*valor+coef_local*feromona_inicial
            
    def run(self):
        for x in range(self.iteraciones):
            camino_it = []
            dist_it = float("inf")
            self.hormigas = self.inicio_hormigas()
            for z in range(self.tamaño-2):
                l = []
                self.mapa_feromona_local = self.mapa_feromona
                for h in self.hormigas:
                    arista = h.run(self.mapa_feromona_local)
                    l.append(arista)
                self.actualizar_feromona_local(l)
            for h in self.hormigas:
                distancia,recorrido = h.obtener_resultados()
                if distancia < self.distancia_mas_corta: 
                    self.distancia_mas_corta = distancia
                    self.mejor_camino = recorrido
                if distancia < dist_it:
                    dist_it = distancia
                    camino_it = recorrido
            self.feromona_hormiga(camino_it,dist_it)
            self.actualizacion_feromona()
            self.mapa_feromonas_hormiga = self.matriz_inicial(0.0)
            if x % 50 == 0:
                print(x,self.distancia_mas_corta)
        return (self.mejor_camino,self.distancia_mas_corta)

hormi = Hormiguero(mapa_dis,feromona_inicial,alpha,beta,coef_disipacion,nhormigas,iteraciones).run()
print(hormi)
   
