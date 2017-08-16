#!/usr/bin/python

import sys, getopt, time, io
import numpy as np
from collections import deque
from array import *

# Punto para bash :D
class colors:
    NC='\033[0m'
    Black='\033[0;30m'
    DarkGray='\033[1;30m'
    Red='\033[0;31m'
    LightRed='\033[1;31m'
    Green='\033[0;32m'
    LightGreen='\033[1;32m'
    BrownOrange='\033[0;33m'
    Yellow='\033[1;33m'
    Blue='\033[0;34m'
    LightBlue='\033[1;34m'
    Purple='\033[0;35m'
    LightPurple='\033[1;35m'
    Cyan='\033[0;36m'
    LightCyan='\033[1;36m'
    LightGray='\033[0;37m'

"""#import datetime
# Public Reloj As Variant
# Public EstadoServidor As Variant
# Public ProximoEvento As Variant
# Public ListaDeEventos(1 To 2) As Variant
# Public Cola(1 To 100) As Variant
# Public TSAcumulado As Variant
# Public DemoraAcumulada As Variant
# Public NroDeClientesEnCola As Variant
# Public AreaQDeT As Variant
# Public TiempoUltimoEvento As Variant
# Public CompletaronDemora As Variant
# Public Paso As Variant
"""

class Simulator(object):

    def __init__(self):
        self.Reloj = 0.0
        self.EstadoServidor = ""
        self.ProximoEvento = ""
        self.ListaDeEventos = array('f')
        self.Cola = array('f')
        self.TSAcumulado = 0.0
        self.DemoraAcumulada = 0.0
        self.NroDeClientesEnCola = 0
        self.AreaQDeT = 0.0
        self.TiempoUltimoEvento = 0.0
        self.CompletaronDemora = 0
        self.Paso = 0
        self.TMEntreArribos = 7.0
        self.TMDeServicio = 9.0
        self.Iniciado = False


    # Sub Inicializar()
    def inicializar(self):

        self.Reloj = 0
        self.EstadoServidor = "D"
        self.ProximoEvento = ""
        #self.ListaDeEventos = [0,0]  qutar

        #
        # ' Vacio el vector que guardar los tiempos de arribo de los clientes a la cola
        #for i in range(100):
        #    self.Cola[i] = 0

        self.TSAcumulado = 0
        self.DemoraAcumulada = 0
        self.NroDeClientesEnCola = 0
        self.AreaQDeT = 0
        self.TiempoUltimoEvento = 0
        self.CompletaronDemora = 0

        # 'Calculo el tiempo de primer arribo
        self.ListaDeEventos.append(valorExponencial(self.TMEntreArribos))
        #
        # 'Fuerza a que el primer evento no sea una partida
        self.ListaDeEventos.append(99999.0)
        self.Paso = 0
        self.Iniciado = False
        self.toString()

    #
    # 'Llamo a la rutina de impresion (al solo efecto de ver como evolucionan los valores de las variables)
    # Call imprimo
    def toString(self):
        print "Valor de la simulacion: "
        print colors.LightCyan+"Relo\t"+colors.NC + str(self.Reloj)
        print colors.LightCyan+"EstadoServidor\t"+colors.NC + str(self.EstadoServidor)
        print colors.LightCyan+"ProximoEvento\t"+colors.NC+ str(self.ProximoEvento)
        print colors.LightCyan+"ListaDeEventos\t"+colors.NC+ str(self.ListaDeEventos)
        print colors.LightCyan+"Cola\t"+colors.NC+ str(self.Cola)
        print colors.LightCyan+"TSAcumulado\t"+colors.NC+ str(self.TSAcumulado)
        print colors.LightCyan+"DemoraAcumulada\t"+colors.NC+ str(self.DemoraAcumulada)
        print colors.LightCyan+"NroDeClientesEnCola\t"+colors.NC+ str(self.NroDeClientesEnCola)
        print colors.LightCyan+"AreaQDeT\t"+colors.NC+ str(self.AreaQDeT)
        print colors.LightCyan+"TiempoUltimoEvento\t"+colors.NC+ str(self.TiempoUltimoEvento)
        print colors.LightCyan+"CompletaronDemora\t"+colors.NC+ str(self.CompletaronDemora)
        print colors.LightCyan+"Paso\t"+colors.NC+ str(self.Paso)
        print colors.LightCyan+"TMEntreArribos\t"+colors.NC+ str(self.TMEntreArribos)
        print colors.LightCyan+"TMDeServicio\t"+colors.NC+ str(self.TMDeServicio)
        print colors.LightCyan+"Iniciado\t"+colors.NC+ str(self.Iniciado)
        print "\n"

    # Sub Principal()
    def run(self):
        # 'Llamo a la rutina de inicializacion
        self.inicializar()

        # Loop Until Reloj >= 8 And NroDeClientesEnCola = 0 And EstadoServidor = "D"
        while True:
            # ' llamada a la rutina de tiempos
            self.tiempos()

            # ' llamada a la rutina correspondiente en funcion del tipo de evento
            # Select Case ProximoEvento
            if self.ProximoEvento == "ARRIBOS":
                self.arribos()
            else:
                self.partidas()

            # ' Llamada a la rutina de imprimo (salo a los fines de ver el estado de las diferentes variables)
            # Call imprimo
            if self.Reloj >= 8 and self.NroDeClientesEnCola == 0 and self.EstadoServidor == "D":
                break


        self.reportes()

    def arribos(self):
        # Todo arribo desencadena un nuevo arribo
        #self.ListaDeEventos[1] = self.Reloj + generarTiempoEntreArribos(0.5)
        self.ListaDeEventos[0] = self.Reloj + valorExponencial(self.TMEntreArribos)
        #
        # 'Pregunto si el servidor esta desocupado
        # If EstadoServidor = "D" Then
        if self.EstadoServidor == "D":
            # ' Cambio el estado del servidor a "Ocupado"
            self.EstadoServidor = "O"

            # ' Programo el proximo evento partida
            self.ListaDeEventos[1] = self.Reloj + valorExponencial(self.TMDeServicio)

            # ' Acumulo el tiempo de servicio
            self.TSAcumulado += (self.ListaDeEventos[1] - self.Reloj)

            # ' Actualizo la cantidad de clientes que completaron la demora
            # CompletaronDemora = CompletaronDemora + 1
            self.CompletaronDemora += 1

        else:
            # 'Calculo el area bajo Q(t) desde el momento actual del reloj hacia atras (TiempoUltimoEvento)
            # AreaQDeT = AreaQDeT + (NroDeClientesEnCola * (Reloj - TiempoUltimoEvento))
            self.AreaQDeT += (self.NroDeClientesEnCola * (self.Reloj - self.TiempoUltimoEvento))

            # ' Incremento la cantidad de clientes en cola en uno (1)
            self.NroDeClientesEnCola += 1

            # 'Guardo el valor del reloj en la posicionn "NroDeClientesEnCola" para saber cuando llegar
            # 'el cliente a la cola y mas adelante calcular la demora.
            # Cola(NroDeClientesEnCola) = Reloj
            #self.Cola[self.NroDeClientesEnCola] = self.Reloj
            self.Cola.append(self.Reloj)

    def partidas(self):
        # ' Pregunto si hay clientes en cola
        if self.NroDeClientesEnCola > 0:
            # ' Tiempo del proximo evento partida
            self.ListaDeEventos[1] = self.Reloj + valorExponencial(self.TMDeServicio)

            # 'Acumulo la demora acumulada como el valor actual del reloj
            # 'menos el valor del reloj cuando el cliente ingresa a la cola
            self.DemoraAcumulada += self.Reloj - self.Cola[0]

            # ' Actualizo el contador de clientes que completaron la demora
            self.CompletaronDemora += 1

            # ' Acumulo el tiempo de servicio
            self.TSAcumulado += (self.ListaDeEventos[1] - self.Reloj)
            #
            # Calculo el Area bajo Q(t) del perriodo anterior (Reloj - TiempoUltimoEvento)
            self.AreaQDeT += (self.NroDeClientesEnCola * (self.Reloj - self.TiempoUltimoEvento))
            #
            # ' Decremento la cantidad de clientes en cola en uno (1)
            self.NroDeClientesEnCola -= 1

            # ' Llamo a la rutina encargada de gestionar la cola
            # ' En este caso debera desplazar todos los valores una posicion hacia adelante
            #self.quitarDeLaCola()
            self.Cola.pop(0)
        else:
            # 'Al no haber clientes en cola, establezco el estado del servidor en "DesOcupado"
            self.EstadoServidor = "D"

            # 'Fuerza a que no haya partidas si no hay clientes atendiendo
            self.ListaDeEventos[1] = 99999.0

    def tiempos(self):
        self.TiempoUltimoEvento = self.Reloj
        if self.ListaDeEventos[0] <= self.ListaDeEventos[1]:
            self.Reloj = self.ListaDeEventos[0]
            self.ProximoEvento = "ARRIBOS"
        else:
            self.Reloj = self.ListaDeEventos[1]
            self.ProximoEvento = "PARTIDAS"
            #print(self.Reloj)

    def reportes(self):
        print colors.LightGreen+'~~~~~~~~~~~~~~~~~~~~~~Reporte~~~~~~~~~~ '+colors.BrownOrange +"Corrida: "+str(0) + colors.NC
        try:
            var1 = self.AreaQDeT / self.Reloj
        except ZeroDivisionError:
            var1 = 0
        print colors.Green+'Nro Promedio Clientes En Cola: '+colors.NC+ str(var1)
        try:
            var2 = self.TSAcumulado / self.Reloj
        except ZeroDivisionError:
            var2 = 0
        print colors.Green+'Utilizacion Promedio Servidores: ' +colors.NC+ str(var2)
        try:
            var3 = self.DemoraAcumulada / self.CompletaronDemora
        except ZeroDivisionError:
            var3 = 0
        print colors.Green+'Demora Promedio Por Cliente: '+colors.NC+ str(var3)

        print colors.Green+'Cantidad Maxima de Clientes en Cola: '+colors.NC+ str(self.NroDeClientesEnCola)

        print colors.LightGreen+'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'+colors.NC

#---------------------------------------------
# Funciones Utiluidades
#---------------------------------------------
def valorExponencial(media):
    return np.random.exponential(media)

"""def quitarDeLaCola(pcola):
    ncola = len(pcola)
    for i in range(ncola):
        pcola[i] = pcola[i + 1]
    pcola[ncola] = ""
"""
#---------------------------------------------
# Progrma, el de consola
#---------------------------------------------

# Globales
name = "Trabajo Practico 1 v0.0"
corridas = 1
outputfile = ''

def load(sim):
    try:
        sim.TMDeServicio = float(input("Ingrese el tiempo medio de servicio: "))
        sim.TMEntreArribos = float(input("Ingrese el tiempo medio entre arribos: "))

    except:
        print colors.Red + "Ingresaste algo no valido...\n" + colors.Yellow + "en caso de ingresar texto use \"text\"" + colors.NC
        sys.exit(2)

def program(argv):
    print colors.Cyan + '~~~~~~~~~~~~~'+name+'~~~~~~~~~~~~~\n' + colors.NC
    try:
        opts, args = getopt.getopt(argv,"ho:c:",["csvfile=","corridas=","debug"])
    except getopt.GetoptError:
        print 'Argumentos no valido pruebe con\n ColaSimple.py -h'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print '~~~~~~~~~~~~~~~~~~~~Argumentos~~~~~~~~~~~~~~~~~~~~'
            print 'Number of arguments:', len(sys.argv), 'arguments.'
            print 'Argument List:', str(sys.argv)
            print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
            sys.exit()
        elif opt in ("-c", "--corridas"):
            corridas = arg
        elif opt in ("-o", "--cvsfile"):
            outputfile = arg
            #print 'guardo en: ', outputfile

#---------------------------------------------
# Ejecucion del modelo
#---------------------------------------------
if __name__ == "__main__":
    program(sys.argv[1:])
    sim1 = Simulator()

    sim1.inicializar()
    load(sim1)
    print colors.Cyan+'~~~~~~~~~~~~~~~~Correr Simulacion~~~~~~~~~~~~~~~~~'

    sim1.run()
