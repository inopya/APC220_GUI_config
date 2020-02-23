# APC220 GUI config
***Configurador para APC220 con interfaz gráfica TKinter compatible Linux/Windows***

Sencillo programa en Python/TKinter para facilitar la configuración de los módulos de comunicaciones APC220 de DFrobot.

Como casi todo en esta vida... surge de la necesidad.

Me dejaron un par de estos módulos para probarlos y no pude hacer funcionar la utilidad RF-Magic que ofrece DFRobot. Asi que hoja de características en mano hice una primera versión muy tosca para programarlos usando un Arduino que enviaba los comandos serie adecuados. Podeis ver dicha versión aqui: https://github.com/inopya/APC220_Transceiver
Me sacó del apuro pero entendí que no era demasiado amigable para que la usasen otros. Asi que he optado por un poco de python y una sencilla interfaz gráfica en tkinter de modo que sea intuitivo y sobre todo compatible con linux.

	Requisitos: Modulos APC220, Arduino Uno (Nano, Micro, Mega...), Python 
	y tener instalada la libreria pyserial: https://pypi.org/project/pyserial/

Grabar Arduino UNO (la opción más comoda debido a que podemos 'pinchar' el APC220 directamente sobre los pines 8 a 13) o cualquier otro Arduino, con el 'firmware' que hay en al carpera ARDUINO_firmware.
La conexión entre Arduino y el módulo APC220 esta descrita en los comentarios del programa *.ino*
Ejecuar en el PC el programa python y a "divertirse"


Breve recordatorio de los parametros de configuración del módulo:
Cuando se lee la configuración del módulo se obtiene un linea similar a esta:

####   ***PARA  AAAAAA B C D E***
####   PARA  415370 2 9 3 0 
	AAAAAA, es la frecuencia de trabajo del modulo expresada en KHz 
	Puede oscilar entre 418MHz y 455MHz
	- en el ejemplo 415370KHz 

	B, es la velocidad de transmisión de radio frecuencia puede tomar los siguientes valores
	1 (2400bps), 2 (4800bps), 3 (9600bps), 4 (19200bps)
	- en el ejemplo 4800bps 
	
	C, es la potencia de emisión, puede tomar valores entre 0 y 9, siendo 9 la mayor potencia
	- en el ejemplo 9 (máxima potencia de emisión 20mW)
	
	D, velodidad de transferencia entre el módulo y Arduino o PC 	, toma valores entre 0 y 6
	0 (1200bps), 1 (2400bps), 2 (4800bps),3 (9600bps), 4 (19200bps), 5 (38400bps), 6 (57600bps)
	- en el ejemplo 9600bps 
	
	E, es el control de paridad de la informacion emitida por RF
	0 (sin control de paridad), 1 (paridad par), 2 (paridad impar)
	- en el ejemplo sin control de paridad
	
Para más detalles consultar el [_datasheet_](./APC220_Datasheet.pdf) que hay en este repositorio o directamente en la página del fabricante.
https://wiki.dfrobot.com/APC220_Radio_Data_Module_SKU_TEL0005_


Para grabar nuevos parametros en el módulo, selecionar desde la interfaz gráfica y pulsar el botón "Grabar configuración"

Comprobar que dicha configuración ha quedado establecida mediante el botón "Leer configuracion"

***
***Ejemplo de la interfaz gráfica del programa junto con la consola python***

![](./imagenes/configuradorAPC220_inopya.png)


***
***Descripción de la interfaz grafica***
![](./imagenes/help.png)


***
***Interfaz grafica con la opcion radioButton desactivada***

Si se desea se pueden motras las opciones de de la intecfaz como botones en lugar de radio botones.
Para ello se ha de utilizar la variable *FLAG_radioButton* que se encuentra al principio del código Python y asignarle el valor *False*  

![](./imagenes/button_mode.png)

***
#  Ejemplos de mensajes durante el uso de programa
***Las siguientes capturas muestran los posibles mensajes y situaciones que nos podemos encontrar durante el uso del programa:***

***
```diff
+Inicio del programa ok, detectado Arduino como programador y APC220 conectado a Arduino
```

![](./imagenes/run_ok.png)

***
```diff
+Inicio del programa con error, detectado Arduino pero APC220 no detectado
```

![](./imagenes/run_fail.png)

*Sugerencia, si no hemos olvidado conectar el módulo, esperar unos segundos y pulsar sobre el boton "Leer configuración"
para que el programa vuelva a detectar el módulo.*

***
```diff
+Lectura correcta de parametros del APC220
```

![](./imagenes/read_ok.png)

***
```diff
+Error en la lectura de parametros del APC220
```

![](./imagenes/read_fail.png)

*Sugerencia, si no hemos olvidado conectar el módulo, esperar unos segundos y pulsar sobre el boton "Leer configuración"
para que el programa vuelva a detectar el módulo.*

***
```diff
+Escritura de nuevos parametros en el APC220 realizada correctamente
```

![](./imagenes/write_ok.png)

***
```diff
+Error al escribir nuevos parametros en el APC220
```

![](./imagenes/write_error.png)

*Sugerencia, si no hemos olvidado conectar el módulo, esperar unos segundos y pulsar sobre el boton "Leer configuración"
para que el programa vuelva a detectar el módulo.*
