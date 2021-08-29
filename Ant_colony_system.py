"""
ANT COLONY SYSTEM
"""
import random
import math
import extraccion_datos




diccionario,mapa_dis = extraccion_datos.principal('./datos/ch130_datos.txt')
tamaño_ciudades = int(diccionario['DIMENSION'])
nombre =  diccionario['NAME']


alpha = 1
beta = 3
coef_disipacion = 0.5
nhormigas= 10
feromona_inicial = nhormigas / 7575.286291798959
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
            self.tamaño = tamaño_ciudades
            self.distancia = 0.0
            self.completo = len(self.recorrido) == self.tamaño
            self.parametro = q0
            self.destinos = posibles_destinos
            
        def run(self,mapa):
            siguiente = self.siguiente_destino(mapa)
            self.distancia += float(self.calculo_distancia(siguiente,self.nodo_actual))
            inicial = self.nodo_actual
            self.nodo_actual = siguiente
            self.destinos.remove(siguiente)
            self.recorrido.append(siguiente)
            return (inicial, self.nodo_actual)

        def calculo_distancia(self,i,h):
            if i < h:
                dis = self.mapa_distancias[i][h]
            else:
                dis = self.mapa_distancias[h][i]
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
                        if math.isnan(x) or (math.isinf(x) and x > 0):
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
                    # acumulacion = 0.0
                    for i in range(len(s)):
                        probabilidad = s[i][1]/float(total)
                        numero -= probabilidad
                        if numero <= 0:
                            fin = False
                            return s[i][0]
                        # acumulacion += s[i][1]
            else:
                maximo = 0.0
                for x in self.destinos:
                    feromona = float(self.mapa_feromonas[a][x])
                    dista = float(self.calculo_distancia(a,x))
                    proba = feromona*pow(1/dista,self.beta)
                    
                    if proba > maximo:
                        maximo = proba
                        elegido = x
                return elegido


    
        def obtener_recorrido(self):
            if len(self.recorrido) == self.tamaño:
                return self.recorrido
            return []
        
        def obtener_distancia(self):
            if len(self.recorrido) == self.tamaño:
                return float(self.distancia)
            return 0.0
        
    
    def __init__(self,mapa_dis,feromona_inicial,alpha,beta,coef_disipacion,nhormigas,iteraciones):
        self.tamaño = tamaño_ciudades
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
        nodo1 = ruta[-1]
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
            for z in range(self.tamaño-1):
                l = []
                self.mapa_feromona_local = self.copiar(self.mapa_feromona)
                for h in self.hormigas:
                    arista = h.run(self.mapa_feromona_local)
                    l.append(arista)
                self.actualizar_feromona_local(l)
            for h in self.hormigas:
                distancia = h.obtener_distancia()
                recorrido = h.obtener_recorrido()
                distancia += h.calculo_distancia(recorrido[0],recorrido[-1])
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
                f.write(str(x)+' '+str(self.distancia_mas_corta)+"\n")
        return (self.mejor_camino,self.distancia_mas_corta)

donde_escribir = nombre+'_ACS.txt'
ruta = './'+nombre+'/'+donde_escribir

f= open(ruta,'w')
for k in range(30):
    f.write("Repetición: "+str(k+1)+"\n")
    print("Repetición",k+1)
    hormi = Hormiguero(mapa_dis,feromona_inicial,alpha,beta,coef_disipacion,nhormigas,iteraciones).run()
    l = []
    for i in hormi[0]:
        l.append(i)
    f.write(str(l)+" "+str(hormi[1])+"\n")#
    print(l,hormi[1])
f.close()
   


