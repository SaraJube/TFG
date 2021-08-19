# -*- coding: utf-8 -*-
"""
ALGORITMO VORAZ

Desde el origen se va a la más cercana y así sucesivamente hasta recorrerlas todas

SOLUCIÓN ENCONTRADA:
    [0, 27, 5, 11, 8, 4, 20, 1, 19, 9, 3, 14, 17, 13, 21, 16, 10, 18, 24, 6, 22, 26, 7, 23, 15, 12, 25, 2]
    8894.929
 
"""

import threading
import math

m1 = [[1.0,1150.0,1760.0],[2.0,630.0,1660.0],[3.0,40.0,2090.0],[4.0,750.0,1100.0],[5.0,750.0,2030.0],
      [6.0,1030.0,2070.0],[7.0,1650.0,650.0],[8.0,1490.0,1630.0],[9.0,790.0,2260.0],[10.0,710.0,1310.0],
      [11.0,840.0,550.0],[12.0,1170.0,2300.0],[13.0,970.0,1340.0],[14.0,510.0,700.0],[15.0,750.0,900.0],
      [16.0,1280.0,1200.0],[17.0,230.0,590.0],[18.0,460.0,860.0],[19.0,1040.0,950.0],[20.0,590.0,1390.0],
      [21.0,830.0,1770.0],[22.0,490.0,500.0],[23.0,1840.0,1240.0],[24.0,1260.0,1500.0],[25.0,1280.0,790.0],
      [26.0,490.0,2130.0],[27.0,1460.0,1420.0],[28.0,1260.0,1910.0],[29.0,360.0,1980.0]]


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

class Hormiguero():
    class Hormiga(threading.Thread):
        def __init__(self,inicio,distancias):
            threading.Thread.__init__(self)
            self.nodo_actual = inicio
            self.mapa_distancias = distancias
            self.recorrido = [inicio]
            self.tamaño = len(distancias)
            self.distancia = 0.0
            self.completo = False
            
        def run(self):
            while len(self.recorrido) < self.tamaño-1:
                siguiente = self.siguiente_destino()
                self.distancia += float(self.mapa_distancias[siguiente][self.nodo_actual])
                self.nodo_actual = siguiente
                self.recorrido.append(siguiente)              
            self.completo = True

        def siguiente_destino(self):
            minimo = 0
            a = self.nodo_actual
            for x in range(self.tamaño-1):
                if not (x==a) and  not(x in self.recorrido):
                    dista = float(self.mapa_distancias[a][x])
                    if minimo != 0:
                        if dista < minimo:
                            minimo = dista
                            siguiente = x
                    else:
                        minimo = dista
                        siguiente = x
            return siguiente

        def obtener_recorrido(self):
            if len(self.recorrido) == self.tamaño-1:
                return self.recorrido
            return []
        
        def obtener_distancia(self):
            if len(self.recorrido) == self.tamaño-1:
                return float(self.distancia)
            return 0.0
        
        def obtener_feromona(self):
            return self.mapa_feromonas
        
    
    def __init__(self,mapa_dis):
        self.tamaño = len(mapa_dis)
        self.mapa_distancia = mapa_dis
        self.distancia_mas_corta = 0.0
        self.mejor_camino = []
        

    def matriz_inicial(self,cte):
        l = []
        for x in range(self.tamaño):
            s = []
            for x in range(self.tamaño):
                s.append(cte)
            l.append(s)
        return l

    def run(self):	
        self.mejor_camino = []
        hormiga =self.Hormiga(0, self.mapa_distancia)
        hormiga.start()
        self.distancia_mas_corta = hormiga.obtener_distancia()
        self.mejor_camino = hormiga.obtener_recorrido()


        return (self.mejor_camino,self.distancia_mas_corta)

hormi = Hormiguero(mapa_dis).run()
print(hormi)