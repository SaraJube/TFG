"""
ALGORITMO GENÉTICO
"""
import math
import random

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

tamañociudades = len(m1)
iteraciones = 40000
npinicial = 10
npadres = 6

def crear_diccionario(lista):
    dic = {}
    for i in range(len(lista)):
        a = int(lista[i][0])
        dic[a]= [lista[i][1],lista[i][2]]
    return dic

datos = crear_diccionario(m1)


class gen():
    
    def __init__(self,ruta):
        self.ruta = ruta
        self.distancia = self.calcular_distancia()
        self.aptitud = 1 / float(self.distancia)
        
    def calcular_distancia(self):
        dis = 0.0
        for i in range(len(self.ruta)-2):
            dis += self.distancia_ciudades(self.ruta[i],self.ruta[i+1])
        dis += self.distancia_ciudades(self.ruta[len(self.ruta)-1],self.ruta[0])
        return dis
    
    
    def distancia_ciudades(self,c1,c2):
        a1 = abs(datos[c1][0]-datos[c2][0])
        a2 = abs(datos[c1][1]-datos[c2][1])
        dis = math.sqrt(a1**2+a2**2)
        return dis
    
    def obtener_distancia(self):
        return self.distancia
    
    def obtener_aptitud(self):
        return self.aptitud
    
    
def crear_poblacion(n,npoblacion):
    ciudades = []
    for i in range(2,n+1):
        ciudades.append(i)
    poblacion = []
    for i in range(npoblacion):
        r = random.sample(ciudades,n-1)
        a = [1]+r
        poblacion.append(a)
    return poblacion

def ordenar_poblacion(poblacion):
    resultados = []
    total = 0.0
    for i in range(len(poblacion)):
        aptitud = gen(poblacion[i]).obtener_aptitud()
        resultados.append((poblacion[i],aptitud))
        total += aptitud
    resultados.sort(key = lambda x: x[1],reverse = True)
    return resultados,total

def seleccion(p,lista,n,total):
    padres = []
    for a in range(n):
        seleccionado = False
        while not seleccionado:
            numero = random.random()
            acumulacion = 0.0
            i = 0
            while i < len(lista) and not seleccionado:
                proba = lista[i][1] / float(total)
                if numero <= proba + acumulacion:
                    padres.append(lista[i][0])
                    a = (lista[i][0],lista[i][1])
                    lista.remove(a)
                    p.remove(lista[i][0])
                    seleccionado = True
                i += 1
    return padres

def copiar(lista):
    l = []
    for i in range(len(lista)):
        l.append(lista[i])
    return l

def cruce(padre1,padre2):
    hijo1 = [0]*len(padre1)
    hijo2 = [0]*len(padre1)
    inicio = random.randint(1, len(padre1))
    fin = random.randint(1, len(padre2))
    copia1 = copiar(padre1)
    copia2 = copiar(padre2)
    for i in range(inicio,fin):
        hijo1[i] = padre1[i]
        copia2.remove(padre1[i])
        hijo2[i] = padre2[i]
        copia1.remove(padre2[i])
        
    for i in range(len(hijo1)):
        if hijo1[i] == 0:
            hijo1[i] = copia2[0]
            copia2.pop(0)
            hijo2[i] = copia1[0]
            copia1.pop(0)
    return hijo1,hijo2

def mutacion(gen):
    corte = random.random()
    for i in range(1,len(gen)):
        if random.random() < corte:
            otro = random.randint(1, len(gen)-1)
            aux = gen[otro]
            gen[otro] = gen[i]
            gen[i] = aux

def reduccion(lista):
    l,a = ordenar_poblacion(lista)
    return l[0:npadres]
    
def principal():
    p = crear_poblacion(tamañociudades,npinicial)
    
    # EMPIEZA EL BUCLE
    for x in range(iteraciones):
        p_ordenado,total = ordenar_poblacion(p)
        # SELECCIÓN DE LOS PADRES
        padres = seleccion(p,p_ordenado,npadres,total)
        i = 0
        hijos = []
        while i < len(padres)-1:
            padre1 = padres[i]
            padre2 = padres[i+1]
            
            # CRUCE
            hijo1,hijo2 = cruce(padre1,padre2)
            # MUTACIÓN
            mutacion(hijo1)
            mutacion(hijo2)
            hijos.append(hijo1)
            hijos.append(hijo2)
            i += 2
        
        # EXTENDER POBLACIÓN
        extension = padres + hijos
        # REDUCIR POBLACIÓN
        mejores = reduccion(extension)
        for i in range(len(mejores)):
            p.append(mejores[i][0])
        if x % 1000 == 0:
            final,a = ordenar_poblacion(p)
            mejor = final[0][0]
            genfinal = gen(mejor)
            print(x,genfinal.distancia)
    final,a = ordenar_poblacion(p)
    mejor = final[0][0]
    genfinal = gen(mejor)
    return genfinal.obtener_distancia(),mejor