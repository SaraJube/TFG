"""
ALGORITMO GENÃ‰TICO
"""

import random
import extraccion_datos


iteraciones = 1000


diccionario,datos = extraccion_datos.principal('./datos/gr202_datos.txt')
tamaño_ciudades = int(diccionario['DIMENSION'])
npinicial = 100
npadres = int(npinicial * 0.3)
nombre =  diccionario['NAME']


class gen():
    
    def __init__(self,ruta,distancias):
        self.ruta = ruta
        self.datos = distancias
        self.distancia = self.calcular_distancia()
        self.aptitud = 1 / float(self.distancia)
        
    def calcular_distancia(self):
        dis = 0.0
        for i in range(len(self.ruta)-1):
            dis += self.calculo_distancia(self.ruta[i],self.ruta[i+1])
        dis += self.calculo_distancia(self.ruta[-1],self.ruta[0])
        return dis
    
    
    def calculo_distancia(self,i,h):
        if i < h:
            dis = self.datos[i][h]
        else:
            dis = self.datos[h][i]
        return dis
    
    def obtener_distancia(self):
        return self.distancia
    
    def obtener_aptitud(self):
        return self.aptitud
    
def obtener_voraz(archivo):
    ruta = './'+nombre+'/'+archivo
    f = open(ruta,'r')
    linea = f.readline()
    info = linea.split(']')
    info[0]= info[0][2:]
    numeros = info[0].split(',')
    a = []
    for num in numeros:
        a.append(int(num))
    f.close()
    return a
    
def obtener_christofides(archivo,poblacion):
    ruta = './'+nombre+'/'+archivo
    f = open(ruta,'r')
    linea = f.readline()
    linea = f.readline()
    for i in range(4):
        info = linea.split(']')
        info[0] = info[0][1:]
        numeros = info[0].split(',')
        a = []
        for num in numeros:
            a.append(int(num))
        poblacion.append(a)
    return poblacion

def crear_poblacion(n,npoblacion):
    ciudades = []
    for i in range(2,n+1):
        ciudades.append(i)
    poblacion = []
    nom = nombre + '_voraz.txt'
    sol_voraz = obtener_voraz(nom)
    poblacion.append(sol_voraz)
    nom = nombre + '_christofides.txt'
    poblacion = obtener_christofides(nom,poblacion)
    for i in range(npoblacion-len(poblacion)):
        r = random.sample(ciudades,n-1)
        a = [1]+r
        poblacion.append(a)
    return poblacion

def ordenar_poblacion(poblacion,datos):
    resultados = []
    total = 0.0
    for i in range(len(poblacion)):
        aptitud = gen(poblacion[i],datos).obtener_aptitud()
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

def reduccion(lista,datos,npadres):
    l,a = ordenar_poblacion(lista,datos)
    return l[0:npadres]
    
def principal(datos,tamaño_ciudades,iteraciones,npinicial,npadres,f):
    p = crear_poblacion(tamaño_ciudades,npinicial)
    # EMPIEZA EL BUCLE
    for x in range(iteraciones):
        p_ordenado,total = ordenar_poblacion(p,datos)
        # SELECCIÃ“N DE LOS PADRES
        padres = seleccion(p,p_ordenado,npadres,total)
        i = 0
        hijos = []
        while i < len(padres)-1:
            padre1 = padres[i]
            padre2 = padres[i+1]
            
            # CRUCE
            hijo1,hijo2 = cruce(padre1,padre2)
            # MUTACIÃ“N
            mutacion(hijo1)
            mutacion(hijo2)
            hijos.append(hijo1)
            hijos.append(hijo2)
            i += 2
        
        # EXTENDER POBLACIÃ“N
        extension = padres + hijos
        # REDUCIR POBLACIÃ“N
        mejores = reduccion(extension,datos,npadres)
        for i in range(len(mejores)):
            p.append(mejores[i][0])
        if x % 50 == 0:
            final,a = ordenar_poblacion(p,datos)
            mejor = final[0][0]
            genfinal = gen(mejor,datos)
            print(x,genfinal.distancia)
            f.write(str(x)+' '+str(genfinal.distancia)+'\n')
    final,a = ordenar_poblacion(p,datos)
    mejor = final[0][0]
    genfinal = gen(mejor,datos)
    return genfinal.obtener_distancia(),mejor

donde_escribir = nombre+'_genetico.txt'
ruta = './'+nombre+'/'+donde_escribir
f = open(ruta,'w')
for k in range(30):
    f.write("Repetición: "+str(k+1)+"\n")
    print("Repetición",k+1)
    a,b = principal(datos,tamaño_ciudades,iteraciones,npinicial,npadres,f)
    l = []
    for i in b:
        l.append(i)
    f.write(str(l)+" "+str(a)+"\n")#
    print(a,b)
f.close()