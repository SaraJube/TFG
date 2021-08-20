"""
ANT COLONY SYSTEM
"""
import random
import math


m1 = [[1.0,1150.0,1760.0],[2.0,630.0,1660.0],[3.0,40.0,2090.0],[4.0,750.0,1100.0],[5.0,750.0,2030.0],
      [6.0,1030.0,2070.0],[7.0,1650.0,650.0],[8.0,1490.0,1630.0],[9.0,790.0,2260.0],[10.0,710.0,1310.0],
      [11.0,840.0,550.0],[12.0,1170.0,2300.0],[13.0,970.0,1340.0],[14.0,510.0,700.0],[15.0,750.0,900.0],
      [16.0,1280.0,1200.0],[17.0,230.0,590.0],[18.0,460.0,860.0],[19.0,1040.0,950.0],[20.0,590.0,1390.0],
      [21.0,830.0,1770.0],[22.0,490.0,500.0],[23.0,1840.0,1240.0],[24.0,1260.0,1500.0],[25.0,1280.0,790.0],
      [26.0,490.0,2130.0],[27.0,1460.0,1420.0],[28.0,1260.0,1910.0],[29.0,360.0,1980.0]]


def dic_distancias(datos):
    l = {}
    for i in datos:
        a = int(i[0])
        c1 = i[1]
        c2 = i[2]
        l[a]=[c1,c2]
    return l
   
mapa_dis= dic_distancias(m1)
alpha = 1
beta = 3
coef_disipacion = 0.5
nhormigas= len(m1)
feromona_inicial = 8894.9285/ nhormigas
print(feromona_inicial)
iteraciones= 1000
coef_local = 0.1
q0 = 0.9

class Hormiguero():
    class Hormiga():
        
        def __init__(self,inicio,distancias, feromonas, alpha, beta,posibles_destinos):
            self.nodo_actual = inicio
            self.mapa_feromonas = feromonas
            self.mapa_distancias = distancias
            self.recorrido = [inicio]
            self.alpha = float(alpha)
            self.beta = float(beta)
            self.tamaño = len(distancias)
            self.distancia = 0.0
            self.completo = len(self.recorrido) == self.tamaño -1
            self.parametro = q0
            self.destinos = posibles_destinos
            
        def run(self,mapa):
            siguiente = self.siguiente_destino(mapa)
            self.distancia += float(self.calculo_distancia(siguiente,self.nodo_actual))
            inicial = self.nodo_actual
            self.nodo_actual = siguiente
            self.destinos.remove(siguiente)
            self.recorrido.append(siguiente)
            self.distancia += float(self.calculo_distancia(self.nodo_actual,self.recorrido[0]))
            return (inicial, self.nodo_actual)

        def calculo_distancia(self,i,h):
            a1 = abs(self.mapa_distancias[i][0]-self.mapa_distancias[h][0])
            a2 = abs(self.mapa_distancias[i][1]-self.mapa_distancias[h][1])
            dis = math.sqrt(a1**2+a2**2)
            return dis
    
        def siguiente_destino(self,mapa):
            q = random.randint(0, 1)
            a = self.nodo_actual
            if q > self.parametro:
                s = []
                total = 0.0
                for x in self.destinos:
                    feromona = float(self.mapa_feromonas[a][x])
                    dista = float(self.calculo_distancia(a,x))
                    proba = pow(feromona,self.alpha)*pow(1/dista,self.beta)
                    total += proba
                    s.append([x,proba])
                total = float(total)

                if total == 0.0:
                    def next_up(x):
                        import struct
                        if math.isnat(x) or (math.isinf(x) and x > 0):
                            return x
                        n = struct.unpack('<q', struct.pack('<d', x))[0]
                        if n >= 0:
                            n += 1
                        else:
                            n -= 1
                        return struct.unpack('<d', struct.pack('<q', n))[0]
					
                    for key in range(len(s)):
                        s[1] = next_up(s[1])
                    total = next_up(total) 
                fin = True
                while fin:
                    numero = random.random()
                    for i in range(len(s)):
                        probabilidad = s[i][1]/float(total)
                        numero -= probabilidad
                        if numero <= 0:
                            fin = False
                            return s[i][0]
            else:
                maximo = 0.0
                for x in self.destinos:
                    feromona = float(self.mapa_feromonas[a][x])
                    dista = float(self.calculo_distancia(a,x))
                    proba =feromona*pow(1/dista,self.beta)
                    if proba > maximo:
                        maximo = proba
                        elegido = x
                return elegido


    
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
        l = {}
        for x in range(1,self.tamaño+1):
            l[x] = {}
            for y in range(1,self.tamaño+1):
               l[x][y] = cte
        return l
    
    
    def actualizacion_feromona(self):
        for x in range(1,self.tamaño+1):
            for y in range(1,self.tamaño+1):
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
    
    def crear_ciudades(self):
        l = []
        for i in range(1,self.tamaño+1):
            l.append(i)
        return l
    
    def inicio_hormigas(self):
        l = []
        for _ in range(self.nhormigas):
            a = random.randint(1,self.tamaño)
            ciudades = self.crear_ciudades()
            ciudades.remove(a)
            hormiga = self.Hormiga(a, self.mapa_distancia, self.mapa_feromona,self.alpha, self.beta,ciudades)
            l.append(hormiga)
        return l
    
    def actualizar_feromona_local(self,l):
        for arista in l:
            a = arista[0]
            b = arista[1]
            valor = self.mapa_feromona_local[a][b]
            self.mapa_feromona_local[a][b] = (1-coef_local)*valor+coef_local*feromona_inicial
            self.mapa_feromona_local[b][a] = (1-coef_local)*valor+coef_local*feromona_inicial
            
    def copiar(self,diccionario):
        l = {}
        for i in diccionario:
            l[i] = diccionario[i]
        return l
    
    def run(self):
        for x in range(self.iteraciones):
            camino_it = []
            dist_it = float("inf")
            self.hormigas = self.inicio_hormigas()
            for z in range(self.tamaño-2):
                l = []
                self.mapa_feromona_local = self.copiar(self.mapa_feromona)
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
   


