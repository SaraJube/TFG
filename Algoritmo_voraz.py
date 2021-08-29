# -*- coding: utf-8 -*-
"""
ALGORITMO VORAZ

Desde el origen se va a la más cercana y así sucesivamente hasta recorrerlas todas

SOLUCIÓN ENCONTRADA:
    [1, 28, 6, 12, 9, 5, 21, 2, 20, 10, 4, 15, 19, 25, 7, 23, 27, 24, 8, 16, 13, 18, 14, 22, 17, 11, 29, 26, 3]
    2005.0
 
"""
import extraccion_datos

diccionario,datos = extraccion_datos.principal('./datos/a280_datos.txt')
tamaño = int(diccionario['DIMENSION'])
nombre =  diccionario['NAME']
inicio = 1

def dic_distancias(datos):
    l = {}
    for x in range(len(datos)):
        nodo = x+1
        l[nodo] = {}
        i = 0
        for y in range(nodo+1,30):
            l[nodo][y] = datos[x][i]
            i += 1
    return l

def crear_ciudades():
    l = []
    for a in range(2,tamaño+1):
        l.append(a)
    return l

def calculo_distancia(i,h,datos):
        if i < h:
            dis = datos[i][h]
        else:
            dis = datos[h][i]
        return dis

def siguiente_destino(a,destinos,datos):
        minimo = 0
        for x in destinos:
            dista = calculo_distancia(a,x,datos)
            if minimo != 0:
                if dista < minimo:
                    minimo = dista
                    siguiente = x
            else:
                minimo = dista
                siguiente = x
        return (siguiente,minimo)
    
    
def voraz(datos):
    destinos = crear_ciudades()
    actual = inicio
    recorrido = [inicio]
    distancia = 0.0
    while destinos:
        siguiente,dis = siguiente_destino(actual,destinos,datos)
        recorrido.append(siguiente)
        distancia += dis
        destinos.remove(siguiente)
        actual = siguiente
    distancia += calculo_distancia(inicio, recorrido[-1],datos)
    return recorrido,distancia

archivo = nombre+'_voraz.txt'
ruta = './'+nombre+'/'+archivo
f = open(ruta,'w')
f.write(str(voraz(datos)))
print(voraz(datos))
f.close()