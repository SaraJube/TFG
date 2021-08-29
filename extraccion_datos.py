# -*- coding: utf-8 -*-
"""
LECTOR TSPLIB
"""


import math

def lector(archivo):
    diccionario = {}
    with open(archivo,'r') as filename:
        linea = filename.readline()
        while linea != 'NODE_COORD_SECTION\n' and linea != 'EDGE_WEIGHT_SECTION\n' :
            info = linea[0:len(linea)-1]
            separado = info.split(':')
            diccionario[separado[0]] = separado[1][1:]
            linea = filename.readline()
        m1 = []
        diccionario['TIPO_DATOS'] = linea[0:-1]
        if linea == 'NODE_COORD_SECTION\n':
            linea = filename.readline()
            while linea !='':
                r = linea.split()
                s=[int(r[0]),float(r[1]),float(r[2])]
                m1.append(s)
                linea = filename.readline()
        elif linea == 'EDGE_WEIGHT_SECTION\n':
            linea = filename.readline()
            while linea != '':
                r = linea.split()
                l = []
                for num in r:
                    l.append(int(num))
                m1.append(l)
                linea = filename.readline()
    return diccionario,m1

def distancia_ciudades(i,j,m1):
    a1 = abs(m1[i-1][1]-m1[j-1][1])
    a2=abs(m1[i-1][2]-m1[j-1][2])
    dis = math.sqrt(a1**2+a2**2)
    return dis

def distancia_geografica(i,j,m1):
    latitude = {}
    longitude = {}
    PI = 3.141592
    deg = int(m1[i-1][1])
    mini = m1[i-1][1] - deg
    latitude[i] = PI * (deg + 5.0 * mini / 3.0 ) / 180.0
    deg = int( m1[i-1][2])
    min = m1[i-1][2] - deg
    longitude[i] = PI * (deg + 5.0 * min / 3.0 ) / 180.0
    
    
    deg = int(m1[j-1][1])
    mini = m1[j-1][1] - deg
    latitude[j] = PI * (deg + 5.0 * mini / 3.0 ) / 180.0
    deg = int( m1[j-1][2])
    min = m1[j-1][2] - deg
    longitude[j] = PI * (deg + 5.0 * min / 3.0 ) / 180.0
    
    RRR = 6378.388
    q1 = math.cos( longitude[i] - longitude[j] )
    q2 = math.cos( latitude[i] - latitude[j] )
    q3 = math.cos( latitude[i] + latitude[j] )
    dij = (int) ( RRR * math.acos( 0.5*((1.0+q1)*q2 - (1.0-q1)*q3) ) + 1.0)
    return dij

def coordenadas(datos,n):
    l = {}
    for nodo in range(1,len(datos)):
        l[nodo] = {}
        i = 0
        for y in range(nodo+1,len(datos)+1):
            if n == 1:
                l[nodo][y] = distancia_ciudades(nodo,y,datos)
            else:
                l[nodo][y] = distancia_geografica(nodo,y,datos)
            i += 1
    return l

def matriz_aristas(datos,tamaño):
    l = {}
    for x in range(len(datos)):
        nodo = x+1
        l[nodo] = {}
        i = 0
        for y in range(nodo+1,tamaño+1):
            l[nodo][y] = datos[x][i]
            i += 1
    return l

def principal(archivos):
    diccionario,m1 = lector(archivos)
    if diccionario['TIPO_DATOS'] == 'NODE_COORD_SECTION':
        if diccionario['EDGE_WEIGHT_TYPE'] == 'EUC_2D':
            mapa_dis= coordenadas(m1,1)
        elif diccionario['EDGE_WEIGHT_TYPE'] == 'GEO':
            mapa_dis= coordenadas(m1,2)     
    else:
        mapa_dis = matriz_aristas(m1,int(diccionario['DIMENSION']))
    return diccionario,mapa_dis
