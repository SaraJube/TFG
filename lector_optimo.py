# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 20:43:31 2021

@author: Sara
"""

with open('a280_ruta_optima.txt') as file:
    linea = file.readline()
    l = []
    while linea != '':
        a = int(linea)
        l.append(a)
        linea =file.readline()
print(l)