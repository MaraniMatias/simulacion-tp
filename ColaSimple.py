#!/usr/bin/python

import sys, getopt, time, io, csv
import numpy as np
from collections import deque
from array import *

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

        self.NroMaximoDeClientesEnCola = 0.0

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
        self.ListaDeEventos.append(999999.0)
        self.Paso = 0
        self.Iniciado = False
        #self.toString()

    #
    # 'Llamo a la rutina de impresion (al solo efecto de ver como evolucionan los valores de las variables)
    # Call imprimo
    def toString(self):
        if True:
            print "Valor de la simulacion: "
            print colors.LightCyan+"Relo\t"+colors.NC+str(self.Reloj)+colors.NC
            print colors.LightCyan+"EstadoServidor\t"+colors.Yellow+str(self.EstadoServidor)+colors.NC
            print colors.LightCyan+"ProximoEvento\t"+colors.Yellow+str(self.ProximoEvento)+colors.NC
            if len(self.ListaDeEventos) <= 15:
                print colors.LightCyan+"ListaDeEventos\t"+colors.Purple+str(np.array(self.ListaDeEventos))+colors.NC
            else:
                print colors.LightCyan+"ListaDeEventos de logitud\t"+colors.Red+str(len(self.ListaDeEventos))+colors.NC
            if len(self.Cola) <= 15:
                print colors.LightCyan+"Cola\t"+colors.Purple+str(np.array(self.Cola))+colors.NC
            else:
                print colors.LightCyan+"Cola de longitud\t"+colors.Red+str(len(self.Cola))+colors.NC

            print colors.LightCyan+"TSAcumulado\t"+colors.NC+str(self.TSAcumulado)+colors.NC
            print colors.LightCyan+"DemoraAcumulada\t"+colors.NC+str(self.DemoraAcumulada)+colors.NC
            print colors.LightCyan+"NroDeClientesEnCola\t"+colors.NC+str(self.NroDeClientesEnCola)+colors.NC
            print colors.LightCyan+"AreaQDeT\t"+colors.NC+str(self.AreaQDeT)+colors.NC
            print colors.LightCyan+"TiempoUltimoEvento\t"+colors.NC+str(self.TiempoUltimoEvento)+colors.NC
            print colors.LightCyan+"CompletaronDemora\t"+colors.NC+str(self.CompletaronDemora)+colors.NC
            print colors.LightCyan+"Paso\t"+colors.NC+str(self.Paso)+colors.NC
            print colors.LightCyan+"TMEntreArribos\t"+colors.NC+str(self.TMEntreArribos)+colors.NC
            print colors.LightCyan+"TMDeServicio\t"+colors.NC+str(self.TMDeServicio)+colors.NC
            print colors.LightCyan+"Iniciado\t"+colors.BrownOrange+str(self.Iniciado)+colors.NC
            print colors.NC+"\n"

    # Sub Principal()
    def run(self):
        # 'Llamo a la rutina de inicializacion
        self.inicializar()

        # Loop Until Reloj >= 8 And NroDeClientesEnCola = 0 And EstadoServidor = "D"
        while not(self.Reloj >= 8 and self.NroDeClientesEnCola == 0 and self.EstadoServidor == "D"):
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
            self.toString()
        # Al salir del while es el fin de la simulacion, emitir reporte
        self.reportes()

    def arribos(self):
        # Todo arribo desencadena un nuevo arribo
        self.ListaDeEventos[0] = self.Reloj + valorExponencial(self.TMEntreArribos)

        # 'Pregunto si el servidor esta desocupado
        if self.EstadoServidor == "D":
            # ' Cambio el estado del servidor a "Ocupado"
            self.EstadoServidor = "O"

            # ' Programo el proximo evento partida
            self.ListaDeEventos[1] = self.Reloj + valorExponencial(self.TMDeServicio)

            # ' Acumulo el tiempo de servicio
            self.TSAcumulado += (self.ListaDeEventos[1] - self.Reloj)

            # ' Actualizo la cantidad de clientes que completaron la demora
            self.CompletaronDemora += 1

        else:
            # 'Calculo el area bajo Q(t) desde el momento actual del reloj hacia atras (TiempoUltimoEvento)
            self.AreaQDeT += (self.NroDeClientesEnCola * (self.Reloj - self.TiempoUltimoEvento))

            # ' Incremento la cantidad de clientes en cola en uno (1)
            self.NroDeClientesEnCola += 1

            # 'Guardo el valor del reloj en la posicionn "NroDeClientesEnCola" para saber cuando llegar el cliente a la cola y mas adelante calcular la demora.
            self.Cola.append(self.Reloj) #self.Cola[self.NroDeClientesEnCola] = self.Reloj

    def partidas(self):
        # ' Pregunto si hay clientes en cola
        if self.NroDeClientesEnCola > 0:
            # ' Tiempo del proximo evento partida
            self.ListaDeEventos[1] = self.Reloj + valorExponencial(self.TMDeServicio)

            # 'Acumulo la demora acumulada como el valor actual del reloj menos el valor del reloj cuando el cliente ingresa a la cola
            self.DemoraAcumulada += self.Reloj - self.Cola[0]

            # ' Actualizo el contador de clientes que completaron la demora
            self.CompletaronDemora += 1

            # ' Acumulo el tiempo de servicio
            self.TSAcumulado += (self.ListaDeEventos[1] - self.Reloj)

            # Calculo el Area bajo Q(t) del perriodo anterior (Reloj - TiempoUltimoEvento)
            self.AreaQDeT += (self.NroDeClientesEnCola * (self.Reloj - self.TiempoUltimoEvento))

            # Guarda la maxima cantidad de clientes en cola
            if self.NroMaximoDeClientesEnCola < self.NroDeClientesEnCola:
                self.NroMaximoDeClientesEnCola = self.NroDeClientesEnCola

            # Decremento la cantidad de clientes en cola en uno (1)
            self.NroDeClientesEnCola -= 1

            # Llamo a la rutina encargada de gestionar la cola, en este caso debera desplazar todos los valores una posicion hacia adelante
            self.Cola.pop(0) #self.quitarDeLaCola()
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
        reporte = Reporte()
        reporte.Observacion = 0
        try:
            reporte.NroPromedioClientesEnCola =  self.AreaQDeT / self.Reloj
        except ZeroDivisionError:
            print ZeroDivisionError
        try:
            reporte.UtilizacionPromedioServidores =  self.TSAcumulado / self.Reloj
        except ZeroDivisionError:
            print ZeroDivisionError
        try:
            reporte.DemoraPromedioPorCliente = self.DemoraAcumulada / self.CompletaronDemora
        except ZeroDivisionError:
            print ZeroDivisionError
        reporte.show()

#---------------------------------------------
# Clase encarda de los reportes
#---------------------------------------------
class Reporte(object):
    def __init__(self):
        self.Observacion = 0
        self.NroPromedioClientesEnCola = 0.0
        self.UtilizacionPromedioServidores = 0.0
        self.DemoraPromedioPorCliente = 0.0
        self.NroMaximoDeClientesEnCola = 0.0

    def show(self):
        print colors.LightGreen+'~~~~~~~~~~~~~~~~~~~~~~Reporte~~~~~~~~~~ '+colors.BrownOrange +"Corrida: "+str(0) + colors.NC
        print colors.Green+'Nro Promedio Clientes En Cola: '+colors.NC+ str(self.NroPromedioClientesEnCola)
        print colors.Green+'Utilizacion Promedio Servidores: ' +colors.NC+ str(self.UtilizacionPromedioServidores)
        print colors.Green+'Demora Promedio Por Cliente: '+colors.NC+ str(self.DemoraPromedioPorCliente)
        print colors.Green+'Cantidad Maxima de Clientes en Cola: '+colors.NC+ str(self.NroMaximoDeClientesEnCola)
        print colors.LightGreen+'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'+colors.NC

    def toCsv(self):
        with open('reporte.csv', 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';', quotechar=';', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['Observaciones','Nro Promedio Clientes En Cola', 'Utilizacion Promedio Servidores', 'Demora Promedio Por Cliente','Cantidad Maxima de Clientes en Cola'])
            spamwriter.writerow([0,])

#---------------------------------------------
# Funciones Utiluidades
#---------------------------------------------
def valorExponencial(media):
    try:
        return np.random.exponential(media)
    except ValueError:
        print colors.Red + str(ValueError) + colors.NC

"""def quitarDeLaCola(pcola):
    ncola = len(pcola)
    for i in range(ncola):
        pcola[i] = pcola[i + 1]
    pcola[ncola] = ""
"""
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
#---------------------------------------------
# Progrma, el de consola
#---------------------------------------------
def load(sim):
    try:
        sim.TMDeServicio = float(input("Ingrese el tiempo medio de servicio: "))
        sim.TMEntreArribos = float(input("Ingrese el tiempo medio entre arribos: "))

    except:
        print colors.Red + "Ingresaste algo no valido...\n" + colors.Yellow + "en caso de ingresar texto use \"text\"" + colors.NC
        sys.exit(2)

def program(argv):
    print colors.Cyan + '~~~~~~~~~~~~~'+name+'~~~~~~~~~~~~~' + colors.NC
    try:
        opts, args = getopt.getopt(argv,"ho:c:",["csvfile=","corridas="])
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
            outputfile = str(arg)
            #print 'guardo en: ', outputfile

#---------------------------------------------
# Ejecucion del modelo
#---------------------------------------------
# Globales
name = "Trabajo Practico 1 v1.2"
corridas = 1
outputfile = 'reporte'

if __name__ == "__main__":
    program(sys.argv[1:])
    sim1 = Simulator()
    sim1.inicializar()
    load(sim1)
    print colors.Cyan+'~~~~~~~~~~~~~~~~Correr Simulacion~~~~~~~~~~~~~~~~~'+ colors.NC

    sim1.run()
#generar 100 observaciones de las variables de respuesta, generando un archivo csv como salida
