#!/usr/bin/python

import sys, getopt, time, io, csv, math
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

    DistribucionVariableTiempoEntreArribos = "exponential"
    DistribucionVariableTiempoServicio = "exponential"

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
        self.gen = Generador()

    # Sub Inicializar()
    def inicializar(self):

        self.Reloj = 0
        self.EstadoServidor = "D"
        self.ProximoEvento = ""
        #self.ListaDeEventos = [0,0]  qutar

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
        self.ListaDeEventos.append(self.gen.valor("arribo",self.TMEntreArribos))

        # 'Fuerza a que el primer evento no sea una partida
        self.ListaDeEventos.append(999999.0)
        self.Paso = 0
        self.Iniciado = False
        #self.toString()

    # 'Llamo a la rutina de impresion (al solo efecto de ver como evolucionan los valores de las variables)
    # Call imprimo
    def toString(self):
        if not Programa.Silencio:
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

            print colors.LightCyan+"Distribucion para la variable tiempo entre arribos: "+colors.NC+Simulator.DistribucionVariableTiempoEntreArribos
            print colors.LightCyan+"Distribucion para la variable tiempo servicio: "+colors.NC+Simulator.DistribucionVariableTiempoServicio
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
        self.ListaDeEventos[0] = self.Reloj + self.gen.valor("arribo",self.TMEntreArribos)
        # Pregunto si el servidor esta desocupado
        if self.EstadoServidor == "D":
            # Cambio el estado del servidor a "Ocupado"
            self.EstadoServidor = "O"
            # Programo el proximo evento partida
            self.ListaDeEventos[1] = self.Reloj + self.gen.valor("servicio",self.TMDeServicio)
            # Acumulo el tiempo de servicio
            self.TSAcumulado += (self.ListaDeEventos[1] - self.Reloj)
            # Actualizo la cantidad de clientes que completaron la demora
            self.CompletaronDemora += 1
        else:
            # 'Calculo el area bajo Q(t) desde el momento actual del reloj hacia atras (TiempoUltimoEvento)
            self.AreaQDeT += (self.NroDeClientesEnCola * (self.Reloj - self.TiempoUltimoEvento))
            # Incremento la cantidad de clientes en cola en uno (1)
            self.NroDeClientesEnCola += 1
            # Guardo el valor del reloj en la posicionn "NroDeClientesEnCola" para saber cuando llegar el cliente a la cola y mas adelante calcular la demora.
            self.Cola.append(self.Reloj) #self.Cola[self.NroDeClientesEnCola] = self.Reloj

    def partidas(self):
        # ' Pregunto si hay clientes en cola
        if self.NroDeClientesEnCola > 0:
            # ' Tiempo del proximo evento partida
            self.ListaDeEventos[1] = self.Reloj + self.gen.valor("servicio",self.TMDeServicio)
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
        reporte.NroMaximoDeClientesEnCola = self.NroMaximoDeClientesEnCola
        reporte.TMDeServicio = self.TMDeServicio
        reporte.TMEntreArribos = self.TMEntreArribos
        try:
            reporte.NroPromedioClientesEnCola =  self.AreaQDeT / self.Reloj
        except ZeroDivisionError:
            reporte.NroPromedioClientesEnCola = 0.0
        try:
            reporte.UtilizacionPromedioServidores =  self.TSAcumulado / self.Reloj
        except ZeroDivisionError:
            reporte.UtilizacionPromedioServidores = 0.0
        try:
            reporte.DemoraPromedioPorCliente = self.DemoraAcumulada / self.CompletaronDemora
        except ZeroDivisionError:
            reporte.DemoraPromedioPorCliente = 0.0
        reporte.show()
        reporte.toCsv()

#---------------------------------------------
# Clase encarda de los reportes
#---------------------------------------------
class Reporte(object):
    outputfile = ""

    def __init__(self):
        self.NroPromedioClientesEnCola = 0.0
        self.UtilizacionPromedioServidores = 0.0
        self.DemoraPromedioPorCliente = 0.0
        self.NroMaximoDeClientesEnCola = 0.0

        # Valores de entrada:
        self.TMDeServicio = 0.0
        self.TMEntreArribos = 0.0

    def show(self):
        if not program.progresbar:
            print colors.LightGreen+'~~~~~~~~~~~~~~~~~~~~~~Reporte~~~~~~~~~~ '+colors.BrownOrange +"Corrida: "+str(Programa.Observacion) +'/'+str(Programa.Corridas)+ colors.NC
            print colors.Yellow+"Variables de entrada:"+colors.NC
            print colors.LightCyan+"Tiempo medio de servicio: "+colors.NC+str(self.TMDeServicio)
            print colors.LightCyan+"Tiempo medio entre arribos: "+colors.NC+str(self.TMEntreArribos)
            print colors.LightCyan+"Distribucion para la variable tiempo entre arribos: "+colors.NC+Simulator.DistribucionVariableTiempoEntreArribos
            print colors.LightCyan+"Distribucion para la variable tiempo servicio: "+colors.NC+Simulator.DistribucionVariableTiempoServicio

            print colors.Yellow+"Variables de respuesta:"+colors.NC
            print colors.Green+'Nro Promedio Clientes En Cola: '+colors.NC+str(self.NroPromedioClientesEnCola)
            print colors.Green+'Utilizacion Promedio Servidores: ' +colors.NC+ str(self.UtilizacionPromedioServidores)
            print colors.Green+'Demora Promedio Por Cliente: '+colors.NC+ str(self.DemoraPromedioPorCliente)
            print colors.Green+'Cantidad Maxima de Clientes en Cola: '+colors.NC+ str(self.NroMaximoDeClientesEnCola)
            print colors.LightGreen+'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'+colors.NC

    def toCsv(self):
        if Reporte.outputfile != "":
            newRow = "%s,%s,%s,%s,%s\n" % (Programa.Observacion,self.NroPromedioClientesEnCola,self.UtilizacionPromedioServidores,self.DemoraPromedioPorCliente,self.NroMaximoDeClientesEnCola)
            if Programa.Observacion <=1:
                # Escribo la cabecera
                with open(Reporte.outputfile+'.csv', 'wb') as csvfile:
                    spamwriter = csv.writer(csvfile, delimiter=';', quotechar=';', quoting=csv.QUOTE_MINIMAL)
                    spamwriter.writerow(['Observaciones','Nro Promedio Clientes En Cola', 'Utilizacion Promedio Servidores', 'Demora Promedio Por Cliente','Cantidad Maxima de Clientes en Cola'])
            # agrego una linea
            with open(Reporte.outputfile+'.csv', 'a') as csvfile:
                csvfile.write(newRow.encode('utf8'))

#---------------------------------------------
# Funciones Utiluidades
#---------------------------------------------
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

class Generador(object):

    def __init__(self):
        self.z0 = int(time.time())

    def getNumAleatorio(self):
        #a = math.pow(7,5)
        #m = math.pow(2,31) - 1
        a = math.pow(5,15)
        m = math.pow(2,35)
        c = 0
        zi = int( a * self.z0 +c ) %  m
        self.z0 = zi
        return zi/m

    def valorExponencial(self,media):
        try:
            return np.random.exponential(media)
        except ValueError:
            print colors.Red + str(ValueError) + colors.NC

    def valorNormal(self,ex=5,vx=1.3):
        try:
            k = 12
            r = 0
            for i in xrange(k):
                r += self.getNumAleatorio()
            z = r - k/2  #/ math.sqrt(k/12)
            return vx * z + ex
        except ValueError:
            print colors.Red + str(ValueError) + colors.NC

    def valorUniforme(self,a=3.5,b=6.5):
        try:
            return a + ( b - a ) + self.getNumAleatorio()
        except ValueError:
            print colors.Red + str(ValueError) + colors.NC

    def valor(self,serviocioArribos,media):
        if serviocioArribos == "arribo":
            if Simulator.DistribucionVariableTiempoEntreArribos == "exponential":
                return self.valorExponencial(media)
            if Simulator.DistribucionVariableTiempoEntreArribos == "normal":
                return self.valorNormal()
            if Simulator.DistribucionVariableTiempoEntreArribos == "uniforme":
                return self.valorUniforme()
        if serviocioArribos == "servicio":
            if Simulator.DistribucionVariableTiempoServicio == "exponential":
                return self.valorExponencial(media)
            if Simulator.DistribucionVariableTiempoServicio == "normal":
                return self.valorNormal()
            if Simulator.DistribucionVariableTiempoServicio == "uniforme":
                return self.valorUniforme()

#---------------------------------------------
# Progrma, el de consola
#---------------------------------------------
class Programa(object):
    Observacion = 0
    Corridas = 1
    Silencio = False

    def __init__(self):
        self.version = "1.5"
        self.name = "Trabajo Practico 1"
        self.TMDeServicio = 0.0
        self.TMEntreArribos = 0.0
        self.progresbar = False

    def distribucionType(self,value=0):
        if value == 1:
            print colors.Purple+"Distribucin Exponencial"+colors.NC
            return "exponential"
        elif value == 2:
            print colors.Purple+"Distribucin Normal, con parametros EX = 5 y VX = 1,3"+colors.NC
            return "normal"
        elif value == 3:
            print colors.Purple+"Distribucin Uniforme, con parametros a = 3,5 y b = 6,5"+colors.NC
            return "uniforme"
        else:
            print "Ingrese numero para identificar diribucion:\n"+colors.LightGray+"\t1- Exponencial\n\t2- Normal\n\t3- Uniforme\n"+colors.NC

    def read(self):
        try:
            self.distribucionType()
            Simulator.DistribucionVariableTiempoEntreArribos = self.distribucionType(int(input('Distribucion para variable tiempo entre arribos: ')))
            if Simulator.DistribucionVariableTiempoEntreArribos == "exponential":
                self.TMEntreArribos = float(input("\tIngrese el tiempo medio entre arribos: "))
            Simulator.DistribucionVariableTiempoServicio = self.distribucionType(int(input('Distribucion variable tiempo de servicio: ')))
            if Simulator.DistribucionVariableTiempoServicio == "exponential":
                self.TMDeServicio = float(input("\tIngrese el tiempo medio de servicio: "))

        except:
            print colors.Red + "Ingresaste algo no valido...\n" + colors.Yellow + "en caso de ingresar texto use \"text\"" + colors.NC
            sys.exit(2)

    def load(self,sim):
        sim.TMDeServicio = self.TMDeServicio
        sim.TMEntreArribos = self.TMEntreArribos

    def getArg(self,argv):
        print colors.Cyan + '~~~~~~~~~~~~~'+self.name+' v'+self.version+'~~~~~~~~~~~~~' + colors.NC
        try:
            opts, args = getopt.getopt(argv,"ho:c:zsp")
        except getopt.GetoptError:
            print 'Argumentos no valido pruebe con\n'+sys.argv[0]+' -h'
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print '~~~~~~~~~~~~~~~~~~~~~Opciones~~~~~~~~~~~~~~~~~~~~~'
                print sys.argv[0]+' [opciones]'
                print '-c -> corridas [-c1]'
                print '-o -> nombre del archivo csv para el reporte [-o"resporte"]'
                print '-s -> no muestra valore sintermedios [-s]'
                print '-p -> bara de progreso en lular de reportes en dada simulacion [-p]'
                print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
                sys.exit()
            elif opt == '-p':
                self.progresbar = True
            elif opt == '-s':
                Programa.Silencio = True
            elif opt == '-c':
                Programa.Corridas = arg
            elif opt == '-o':
                Reporte.outputfile = str(arg)
            elif opt == '-z':
                print '~~~~~~~~~~~~~~~~~~~~Argumentos~~~~~~~~~~~~~~~~~~~~'
                print " opt: "+ str(opt) + "arg: "+str(arg)
                print 'Number of arguments:', len(sys.argv), 'arguments.'
                print 'Argument List:', str(sys.argv)
                print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
                sys.exit()

#---------------------------------------------
# Ejecucion del modelo
#---------------------------------------------
if __name__ == "__main__":
    program = Programa()
    program.getArg(sys.argv[1:])
    program.read()
    sim = Simulator()
    gen = Generador()
    print colors.Cyan+'~~~~~~~~~~~~~~~~Correr Simulacion~~~~~~~~~~~~~~~~~'+ colors.NC

    if program.progresbar:
        toolbar_width = 50
        #sys.stdout.write("[%s] %s/%s 0%%" % (" " * toolbar_width,Programa.Observacion,Programa.Corridas))
        sys.stdout.write("[%s]" % (" " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width+2))

    for x in xrange(int(Programa.Corridas)):
        Programa.Observacion += 1
        sim.inicializar()
        program.load(sim)
        sim.run()

        if program.progresbar:
            porcent = int(Programa.Observacion) * 100 / int(Programa.Corridas)
            bar = porcent * int(toolbar_width) / 100
            #sys.stdout.write("[%s%s] %s/%s %s%%" % ("="*bar," " * (toolbar_width - bar),Programa.Observacion,Programa.Corridas,porcent))
            sys.stdout.write("[%s%s]" % ("="*bar," " * (toolbar_width - bar)))
            sys.stdout.flush()
            sys.stdout.write("\b" * (toolbar_width+2))

    if program.progresbar:
        sys.stdout.write("\n")

    if Reporte.outputfile != "":
        print colors.LightBlue+"Guardado en: %s.csv" % (Reporte.outputfile)+colors.NC

