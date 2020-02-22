#!/usr/bin/python
# -*- coding: utf-8 -*-


#       _\|/_   A ver..., ¿que tenemos por aqui?
#       (O-O)        
# ---oOO-(_)-OOo---------------------------------
 
 
##########################################################
# ****************************************************** #
# *            DOMOTICA PARA PRINCIPIANTES             * #
# *      TKinter GUI para configuracion de APC220      * #
# *                                                    * #
# *          Autor:  Eulogio López Cayuela             * #
# *                                                    * #
# *     APC220 TK GUI  v1.0   Fecha: 13/02/2020        * #
# ****************************************************** #
##########################################################


#--------------------------------------------------------
# IMPORTACION DE BIBLIOTECAS
#--------------------------------------------------------

# TIEMPOS, FECHAS
import time             #manejo de funciones de tiempo (fechas, horas, pausas...)
from time import sleep  #pausas...

#PUERTO SERIE
import serial


#ENTORNO GRAFICO TKinter
try:
    from tkinter import *

except ImportError:
    from Tkinter import *



FLAG_radioButton = True  #selecciona entre radioboton o bonton normal en los menus de parametros



class StatusBar(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)#anchor=E
        self.label.pack(fill=X)

    def text_color(self, format, *args):
       self.label.config(fg=format % args)
       self.label.update_idletasks()
        
    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()
        

# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# FUNCIONES ARDUINO / SERIAL
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

def detectarPuertoArduino():   #version mejorada 2018
    '''
    Funcion para facilitar la deteccion del puerto Serie en distintos sistemas operativos
    Escanea los posibles puertos y retorna el nombre del puerto con el que consigue comunicarse
    '''

    #Reconocer el tipo de sistema operativo
    sistemaOperativo = sys.platform
    
    #Definir los prefijos de los posibles puertos serie disponibles tanto en linux como windows
    puertosWindows = ['COM']
    puertosLinux = ['/dev/ttyUSB', '/dev/ttyACM', '/dev/ttyS', '/dev/ttyAMA','/dev/ttyACA']
    
    puertoSerie = ''
    if (sistemaOperativo == 'linux' or sistemaOperativo == 'linux2'):
        listaPuertosSerie = puertosLinux
        index = 0
    else:
        listaPuertosSerie = puertosWindows
        index = 4  # Windows suele reservar los 3 primeros puertos. Cambiar este indice si no detectamos nada
        
    for sufijo in listaPuertosSerie:
        for n in range(index, 35):
            try:
                # intentar crear una instancia de Serial para 'dialogar' con ella
                nombrePuertoSerie = sufijo + '%d' %n
                print ("Probando... ", nombrePuertoSerie)
                time.sleep(.1)
                serialTest = serial.Serial(nombrePuertoSerie, VELOCIDAD_PUERTO_SERIE)
                serialTest.close()
                return nombrePuertoSerie

            except:
                pass
        
    return '' #si llegamos a este punto es que no hay Arduino disponible

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------  

def consultar_Arduino(PAUSA = 0.5):
    '''
    Funcion para acceso a ARDUINO y obtencion de datos en tiempo real   ---
    version mejorada para evitar errores de comunicacion
    ante eventuales fallos de la conexion.
    '''
    global arduinoSerialPort, FLAG_APC_presente

    try:
        arduinoSerialPort.flushInput() #eliminar posibles restos de lecturas anteriores
        arduinoSerialPort.flushOutput()#abortar comunicaciones salientes que puedan estar a medias

    except:
        print ("\nError borrando datos del puerto Serie de Arduino")
 
    try:
        time.sleep(PAUSA)
        #revisar si hay datos en el puerto serie
        if (arduinoSerialPort.inWaiting()>0):  
            #leer una cadena desde el el puerto serie y 'despiojarla'
            linea_leida_de_Arduino = arduinoSerialPort.readline().strip()
            linea_leida_de_Arduino = linea_leida_de_Arduino.decode("utf-8")
            try:
                return  linea_leida_de_Arduino
            except:
                return None
    except:
        #si llegamos aqui es que se ha perdido la conexion con el APC o peor aun... con Arduino  :(
        print ("\n_______________________________________________")
        print ("\n == APC NO DETECTADO o FALLO CONEXION DE ARDUINO == ")
        print ("\n Espere unos segundos e intentelo de nuevo")
        print (" Si el fallo persite cierre el programa,\n reconecte arduino y ejecute de nuevo \n\n\n\n")
        FLAG_APC_presente = False

    return None 

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------  

def enviar_a_Arduino(orden):
    ''' funcion para enviar ordenes a ARDUINO '''
    global arduinoSerialPort

    try:
        arduinoSerialPort.flushInput() #eliminar posibles restos de lecturas anteriores
        arduinoSerialPort.flushOutput()#abortar comunicaciones salientes que puedan estar a medias

    except:
        print ("---------------------------")
        print ("error borrando datos del puerto Serie de Arduino")
        
    if(len(orden) < 2):
        return False
     
    orden_envio = str(orden)
    orden_envio = orden_envio.encode('utf-8')
    
    try:
        
        arduinoSerialPort.write(orden_envio)
        return True
        
    except:
        #si llegamos aqui es que se ha perdido la conexion con Arduino  :(
        print ("\n_______________________________________________")
        print ("\n == CONEXION CON ARDUINO PERDIDA == ")
        print ("\n Cierre el programa, reconecte arduino y ejecute de nuevo \n\n\n\n")
        root.destroy()

    return None   # notificamos un problema 


# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# FUNCIONES EVENTOS TKinter
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm


def select_flag(flag):
    global FLAG_APC_presente
    
    if flag==0:
        mensaje = ""
        print("\nRECIBIDA ORDEN GRABAR")
        comando = update_info()
        print(comando)
        print("\nARDUINO esta procesando...\n\n")
        enviar_a_Arduino(comando)
        sleep(2)
        enviar_a_Arduino("RD")  ##nuevo
        respuesta = consultar_Arduino(2) ##nuevo
        listaRespuesta = respuesta.split(" ")##nuevo
        if (len(listaRespuesta) == 6):##nuevo
            #respuesta de parametros ok
            if (listaRespuesta[0] == "PARA"):
                mensaje = "WRITE:  "+ respuesta + "  ,ok"
                print("\n >> CONFIGURACION ACTUALIZADA\n\n")
        else:
            mensaje = "WRITE ERROR"
            print("\n >> FALLO ACTUALIANDO CONFIGURACION\n\n")
            FLAG_APC_presente  = False
        config_label.configure(fg="red", text=mensaje)
        
        
    if flag==1:
        print("\nRECIBIDA ORDEN LEER ")
        print("\nARDUINO esta procesando...\n\n")
        enviar_a_Arduino("RD")
        respuesta = consultar_Arduino(2)

        if (respuesta == "APC_FAIL"):
            print("MODULO NO DETECTADO, REVISE LAS CONEXIONES")
            mensaje = "MODULO NO DETECTADO"
            config_label.configure(fg="red", text=mensaje)
            FLAG_APC_presente  = False
            return

        if (respuesta != None):
            print(respuesta)
            listaRespuesta = respuesta.split(" ")
            if (len(listaRespuesta) == 6 and listaRespuesta[0] == "PARA"):
                FLAG_APC_presente  = True
                mensaje = "READ:  "+ respuesta
                config_label.configure(fg="green", text=mensaje)
            return

        if (respuesta == None):
            pass#FLAG_APC_presente  = False    

def mouse_click(event):
    update_info()
    return


def update_info():
    info_status_bar = ""
    a = w0.get()
    if a<418:
        a=418
    if a>=455:
        a=455
        w1.set(0)
        w2.set(0)
    b1 = int(w1.get()/100)
    b2= w2.get()
    ajuste =""
    if b2 <10:
        ajuste ="0"
    c = bitrateRF.get()
    d = potenciaRF.get()
    e = bitrateSerial.get()
    f = paridad.get()
    RadioFrecuencia  = str(a)+str(b1)+ajuste+str(b2)
    if(int(RadioFrecuencia))>455000:
       RadioFrecuencia = "455000"
    comando = "WR "+RadioFrecuencia+" "+str(c)+" "+str(d)+" "+str(e)+" "+str(f)
    MHz_label.configure(text=comando)

    if(FLAG_APC_presente  == True):
        info_status_bar = info_puerto_conexion + "  --> Modulo APC220, ok"
        statusbar.text_color("blue")
        
    if(FLAG_APC_presente  == False):
        info_status_bar = info_puerto_conexion + "  --> Modulo APC220 no detectado"
        statusbar.text_color("red")
    statusbar.set(info_status_bar)
    
    root.after(100, update_info)
    
    return comando


#----------------------------------------------------------------------------------------------------
#  FIN DEL BLOQUE DE DEFINICION DE FUNCIONES
#----------------------------------------------------------------------------------------------------


VELOCIDAD_PUERTO_SERIE = 9600

SerialDelay = 0.5                   #tiempo entre llamadas del puerto (en segundos), para que pueda reaccionar.
                                    #No usar tiempos inferiores a 0.25 segundos 

#====================================================================================================
# PUERTO SERIE PARA COMUNICACION CON ARDUINO
#====================================================================================================
# Crear una instancia de Serial para 'dialogar' con Arduino
'''
En este bloque creamos una instancia al puerto donde se conecta arduino y verificamos su validez.
Tambien se encarga de vigilar eventuales fallos de conexion y evitar los bloqueos del programa,
encargandose de gestionar la reconexion de arduino incluso aunque esta se haga en un puerto distinto
del que se conecto inicialmente
'''

FLAG_reinicio = True
FLAG_APC_presente  = False
mensajeAPCpresente = ""


puertoDetectado = detectarPuertoArduino() #detactamos automaticamente el puerto

sleep(2)

if (puertoDetectado != ''):
    arduinoSerialPort = serial.Serial(puertoDetectado, VELOCIDAD_PUERTO_SERIE) #usamos el puerto detectado
    print ("\n ** PLC Conectado en " + puertoDetectado + " ** \n")
    
    print("\n >> Comprobando conexion APC220\n")

    #sleep(8)
    n=0
    while (n<5 and FLAG_APC_presente == False):  # a veces tarda un poco en contestarnos la primera vez
        n+=1
        enviar_a_Arduino("ID")
        mensajeAPCpresente = consultar_Arduino(2)
        if (mensajeAPCpresente == "APC_OK"):   # "APC_FAIL"  respuesta si no lo encuentra
            FLAG_APC_presente = True
    print("FLAG_APC_presente: ", FLAG_APC_presente," --> ", mensajeAPCpresente)
    print("\n\n")   
   
else:
    print (" == GRABADOR APC220 NO PRESENTE == ")
    print ("    conecte un PLC compatible antes de 120 segundos\n")

    tiempoInicio = time.time()
    ActualTime = time.time()
    while (ActualTime - tiempoInicio < 120): 
        puertoDetectado = detectarPuertoArduino() #detactamos automaticamente el puerto
        ActualTime = time.time()
        if (puertoDetectado != ''):
            arduinoSerialPort = serial.Serial(puertoDetectado, VELOCIDAD_PUERTO_SERIE) #usamos el puerto detectado
            print ("\n ** PLC Conectado en " + puertoDetectado + " ** ")
            break

if (puertoDetectado == ''):
    print ("\n == CONECTE UN PLC COMPATIBLE Y REINICIE EL PROGRAMA == \n")


'''
PARAM AAAAAA B C D E
PARAM 415370 2 9 3 0

AAAAAA, es la frecuencia de trabajo del modulo expresada en KHz 
Puede oscilar entre 418MHz y 455MHz
- en el ejemplo 415.37MHz 

B, es la velocidad de transmision de radio frecuencia puede tomar los siguientes valores
1 (2400bps), 2 (4800bps), 3 (9600bps), 4 (19200bps)
- en el ejemplo 4800bps 

C, es la potencia de emision, puede tomar valores entre 0 y 9, siendo 9 la mayor potencia
- en el ejemplo 9 (maxima potencia de emision)

D, velodidad de transferencia entre el modulo y arduino o PC 	, toma valores entre 0 y 6
0 (1200bps), 1 (2400bps), 2 (4800bps),3 (9600bps), 4 (19200bps), 5 (38400bps), 6 (57600bps)
- en el ejemplo 9600bps 

E, es el control de paridad de la informacion emitida por RF
0 (sin control de paridad), 1 (paridad par), 2 (paridad impar)
- en el ejemplo sin control de paridad


'''


# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# =========================================================================================================
#   INICIO DE CONTROL DE CAMARA 
# =========================================================================================================
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

if puertoDetectado:
    ''' Entramos aqui solo si se ha detectado una placa arduino o PLC compatible '''                                                              
            
    print ("FECHA y HORA DEL REINICO DEL PROGRAMA:   ", time.strftime("%Y/%m/%d-%H:%M:%S", time.localtime(time.time()))) #hora local)
    print ("\n\n")


    info_puerto_conexion = "ARDUINO Programador APC220 en puerto: " + puertoDetectado

    # initialize the window toolkit along with the two image panels
    root = Tk()
    root.title("CONFIGURADOR modulos APC220 Linux/Windows - Inopya")
    root.resizable(False, False)

    statusbar = StatusBar(root)
    statusbar.pack(side=BOTTOM, fill=X)
    statusbar.set(info_puerto_conexion)
    
    screen_nombres = Frame(root)
    screen_medio = Frame(root)
    
    panel_bitrateRF = Frame(root)
    panel_potenciaRF = Frame(root)
    panel_bitrateSerial = Frame(root)
    panel_paridad = Frame(root)
    
    panel_MHz = Frame(root)
    screen_info = Frame(root)
    screen_botones = Frame(root)
    screen_lectura = Frame(root)
    

    paridad_label = Label(screen_nombres, text="  bitrate RF   ")
    #paridad_label.pack(side="left")
    paridad_label.grid(row=0,column=0)
    
    paridad_label = Label(screen_nombres, text="Potencia RF ")
    paridad_label.grid(row=0,column=1)

    paridad_label = Label(screen_nombres, text="   bitrate Serial  ")
    paridad_label.grid(row=0,column=2)

    paridad_label = Label(screen_nombres, text="   Paridad")
    paridad_label.grid(row=0,column=3)


    # *** BITRATE RF *** 
    bitrateRF = IntVar()
    for text, value in [(' 2400 bps  ', 1), (' 4800 bps  ', 2), (' 9600 bps  ', 3), ('19200 bps  ', 4)]:
        if(FLAG_radioButton==True):
            Radiobutton(panel_bitrateRF, text=text, value=value, variable=bitrateRF).pack(anchor=W)
        else:
            Radiobutton(panel_bitrateRF, text=text, value=value, variable=bitrateRF, indicatoron=0).pack(anchor=W, fill=X, ipadx=18)
    bitrateRF.set(3)


    # *** POTENCIA DE EMISION ***
    potenciaRF = IntVar()
    for text, value in [('0      ',0),('1      ',1),('2      ',2),('3      ',3),('4      ',4),('5      ',5),('6      ',6),('7      ',7),('8      ',8),('9      ',9),]:
        if(FLAG_radioButton==True):
            Radiobutton(panel_potenciaRF, text=text, value=value, variable=potenciaRF).pack(anchor=CENTER)
        else:
            Radiobutton(panel_potenciaRF, text=text, value=value, variable=potenciaRF, indicatoron=0).pack(anchor=W, fill=X, ipadx=18)
    potenciaRF.set(9)
    
    
    # *** BITRATE SERIAL - ARDUINO ***
    bitrateSerial = IntVar()
    for text, value in [('  1200 bps  ', 0),('  2400 bps  ', 1),('  4800 bps  ', 2),('  9600 bps  ', 3),('19200 bps  ', 4),('38400 bps  ', 5),('57600 bps  ', 6),]:
        if(FLAG_radioButton==True):
            Radiobutton(panel_bitrateSerial, text=text, value=value, variable=bitrateSerial).pack(anchor=E)
        else:
            Radiobutton(panel_bitrateSerial, text=text, value=value, variable=bitrateSerial, indicatoron=0).pack(anchor=W, fill=X, ipadx=18)
    bitrateSerial.set(3)


    # *** PARIDAD ***
    paridad = IntVar()
    for text, value in [('Sin Paridad', 0), ('Paridad PAR', 1),('Paridad IMPAR', 2),]:
        if(FLAG_radioButton==True):
            Radiobutton(panel_paridad, text=text, value=value, variable=paridad).pack(anchor=W)
        else:
            Radiobutton(panel_paridad, text=text, value=value, variable=paridad, indicatoron=0).pack(anchor=W, fill=X, ipadx=18)
    paridad.set(0)

    
    # *** FRECUENCIA DE LA EMISION RF ***
    w0 = Scale(panel_MHz, from_=418, to=455, resolution=1, length=350, orient=HORIZONTAL)
    w0.bind("<ButtonRelease-1>", mouse_click)#
    w0.pack(side="top", padx=10, pady=2)
    w0.set(0)
    
    w2 = Scale(panel_MHz, from_=0, to=99, resolution=1, length=350, orient=HORIZONTAL)
    w2.bind("<ButtonRelease-1>", mouse_click)#
    w2.pack(side="bottom", padx=10, pady=2)
    w2.set(0)
    
    w1 = Scale(panel_MHz, from_=0, to=900, resolution=100, length=350, orient=HORIZONTAL)
    w1.bind("<ButtonRelease-1>", mouse_click)#
    w1.pack(side="bottom", padx=10, pady=2)
    w1.set(0)
    
  
    MHz_label = Label(screen_info, bg="white", fg="blue", text="")
    MHz_label.pack()

    config_label = Label(screen_lectura, text="", fg="Red", font=("Helvetica", 16))
    config_label.pack()
    
    update_info()
    
    if(FLAG_reinicio == True):
        FLAG_reinicio = False
        if(FLAG_APC_presente  == False):
            config_label.configure(fg="red", text="APC220, fail")
        else:
            config_label.configure(fg="blue", text="APC220, ok")
            
    boton_grabar = Button(screen_botones, text="Grabar configuracion", command= lambda:select_flag(0))
    boton_grabar.pack(side="left", padx="10", pady="10")

    boton_leer = Button(screen_botones, text="Leer configuracion", command= lambda:select_flag(1))
    boton_leer.pack(side="right", fill="none", expand="no", padx="10", pady="10")


    screen_nombres.pack(fill=X)

    panel_bitrateRF.pack(side="left",anchor=N)
    panel_potenciaRF.pack(side="left",anchor=N)
    panel_bitrateSerial.pack(side="left",anchor=N)
    panel_paridad.pack(side="left",anchor=N)

    panel_MHz.pack(fill=X)
    screen_info.pack(fill=X)
    screen_botones.pack()
    screen_lectura.pack()

    root.mainloop()
