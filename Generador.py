#!/usr/bin/python

import numpy as np
import sys, getopt, time, io, csv, math

class Generador(object):

    def __init__(self):
        self.z0 = int(time.time())

    def getNumAleatorio(self):
        try:
            #a = math.pow(7,5)
            #m = math.pow(2,31) - 1
            a = math.pow(5,15)
            m = math.pow(2,35)
            c = 0
            zi = int( a * self.z0 +c ) %  m
            self.z0 = zi
            r = zi/m
            if r < 0 and 1 < r:
                raise ValueError('Rando mal generado. => ' + str(r))
            return r
        except ValueError:
            print colors.Red + str(ValueError) + colors.NC

    def valorExponencial(self,media):
        try:
            return np.random.exponential(media)
        except ValueError:
            print colors.Red + str(ValueError) + colors.NC

    def valorNormal(self,ex=5,vx=1.3):
        try:
            # Ahora para una distribucion no estandar
            r = 0
            for i in xrange(12):
                r += self.getNumAleatorio()
            x = vx * (r - 6) + ex
            #return np.random.normal(ex,vx)
            return x
        except ValueError:
            print colors.Red + str(ValueError) + colors.NC

    def valorUniforme(self,a=3.5,b=6.5):
        try:
            x =  a + ( b - a ) * self.getNumAleatorio()
            if not ( a < x and x < b):
                raise ValueError('No es uniforme. => ' + str(x))
            #return np.random.uniform(a,b)
            return x
        except ValueError:
            print colors.Red + str(ValueError) + colors.NC

gen = Generador()

for x in xrange(100):
    #print gen.valorUniforme()
    print gen.valorNormal()
