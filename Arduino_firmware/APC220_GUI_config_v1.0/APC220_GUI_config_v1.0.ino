
/*
  #       _\|/_   A ver..., ¿que tenemos por aqui?
  #       (O-O)        
  # ---oOO-(_)-OOo---------------------------------
   
   
  ##########################################################
  # ****************************************************** #
  # *            DOMOTICA PARA AFICIONADOS               * #
  # *     Tk GUI  Configuracion del modulo APC220        * #
  # *          Autor:  Eulogio López Cayuela             * #
  # *                                                    * #
  # *       Versión v1.0      Fecha: 13/02/2020          * #
  # ****************************************************** #
  ##########################################################
*/

#define __VERSION__ "\Tk GUI Configuracion del modulo APC220 v1.0\n"

/*
  
 ===== NOTAS DE LA VERSION =====
 
 >> Cuando se lee la configuracion del modulo se obtiene un linea similar a esta (PARAM 415370 2 9 3 0 )

"PARA AAAAAA B C D E"

	AAAAAA, es la frecuencia de trabajo del modulo expresada en KHz 
	Puede oscilar entre 418MHz y 455MHz
	- en el ejemplo 415.370 MHz 

	B, es la velocidad de transmision de radio frecuencia puede tomar los siguientes valores
	1 (2400bps), 2 (4800bps), 3 (9600bps), 4 (19200bps)
	- en el ejemplo 4800bps
	
	C, es la potencia de emision, puede tomar valores entre 0 y 9, siendo 9 la mayor potencia
	- en el ejemplo 9
	
	D, velodidad de transferencia entre el modulo y arduino o PC 	, toma valores entre 0 y 6
	0 (1200bps), 1 (2400bps), 2 (4800bps),3 (9600bps), 4 (19200bps), 5 (38400bps), 6 (57600bps)
	- en el ejemplo 9600bps
	
	E, es el control de paridad de la informacion emitida por RF
	0 (sin control de paridad), 1 (paridad par), 2 (paridad impar)
  - sin control de paridad

>> Para grabar informacion se ha de enviar una linea similar...
   WR 434000 3 9 3 0

  Esta configuracion seria: Frecuencia de emision 434MHz, velocidad RF 9600, 
  maxima potencia, Puerto serie 9600 y sin control de paridad
 
*/


/*
  CONEXIONES:

 =======================
  ARDUINO     APC220
 =======================
   GND  --->   GND  
   D13  --->   Vcc
   D12  --->   EN
   D11  --->   RX  
   D10  --->   TX
   D09  --->   AUX 
   D08  --->   SET 
   
*/ 


/*mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
//        IMPORTACION DE LIBRERIAS
//mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm*/

#include <SoftwareSerial.h>



/*mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
//        SECCION DE DECLARACION DE CONSTANTES  Y  VARIABLES GLOBALES
//mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm*/

//------------------------------------------------------
//Definiciones para pines y variables
//------------------------------------------------------
#define SET      8
#define AUX      9
#define TDX     10
#define RDX     11
#define EN      12 
#define VCC     13


SoftwareSerial APCport(TDX, RDX);  //definimos el puerto serie Software para comunicar con el modulo RF


boolean FLAG_estado_led = false;


//mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm 
//***************************************************************************************************
//         FUNCION DE CONFIGURACION
//***************************************************************************************************
//mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm 

void setup() 
{
  Serial.begin(9600);
  //Serial.println(F(__VERSION__));
  
  APCport.begin(9600);  //iniciar el puerto serie software para comunicar con el APC220
  
  pinMode(SET,OUTPUT);
  pinMode(AUX,INPUT);
  pinMode(EN,OUTPUT);
  pinMode(VCC,OUTPUT);

  digitalWrite(SET,HIGH);
  digitalWrite(VCC,HIGH);
  digitalWrite(EN,HIGH);

  //delay(1000);
  
  //Serial.println(F("CONFIGURACION ACTUAL:\n"));
  //read_config();

}

  

//mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm 
//***************************************************************************************************
//  BUCLE PRINCIPAL DEL PROGRAMA   (SISTEMA VEGETATIVO)
//***************************************************************************************************
//mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm 

void loop() 
{
  atenderPuertoSerie();
}



/*mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
   ###################################################################################################### 
        BLOQUE DE FUNCIONES: LECTURAS DE SENSORES, COMUNICACION SERIE, CONTROL LCD...
   ###################################################################################################### 
//mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm*/


/*mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
//    COMUNICACIONES (PUERTO SERIE) 
//mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm*/

//========================================================
// FUNCION PARA LECTURA DE CADENAS POR PUERTO SERIE
//========================================================

void atenderPuertoSerie() 
{
  String cadena_recibida = "";
  while(Serial.available()) {
    cadena_recibida = Serial.readString();  // leer una cadena 
  }
  cadena_recibida.trim();                   //eliminamos los posibles espacios en blanco al inicio y final de la cadena
  
  if (cadena_recibida.length() >0) {
    cadena_recibida.toUpperCase();
    String comando = cadena_recibida.substring(0,2);
    
    /* leer configuracion y enviarla al puerto serie */
    if(comando=="RD"){
      read_config();
      return;
    }    


    /* comprobar si al modulo esta conectado */
    if(comando=="ID"){
      mostrar_ID(); 
      return;
    }
    
    /* Escribir una configuracion en el transceptor */
    if(comando=="WR"){
      
      /* comprobar que la configuracion recibida es valida ants de grabarla */
      //Codigo para validar el comando recibido si se desea.
      //Lo validamos en python antes del envio, pero por si queremos redundar...
      
      /* grabar la nueva configuracion */
      write_config(cadena_recibida);        // consultar el datasheet para detalle de los parametros
      
      /* esperar un poco... */
      delay(1000);
      return;
    }
  }       
}



/*mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
//  LEER Y GRABAR CONFIGURACION EN EL APC220
//mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm*/

//========================================================
// INDICAR SI HAY APC CONECTADO
//========================================================

void mostrar_ID()
{
  digitalWrite(SET, LOW);         // poner en modo configuracion
  delay(50);                      // pausa para estabilizar
  APCport.print("RD");            // peticion de datos
  APCport.write(0x0D);            // fin de linea
  APCport.write(0x0A);            // y retorno de carro. Similar a hacer un 'println', pero con println no funciona :(
  delay(200);                     // pausa para estabilizar

  bool FLAG_APC_presente = false;
  while (APCport.available()) {
    FLAG_APC_presente = true;
    char c = APCport.read();
  }
  digitalWrite(SET, HIGH);        // volver al modo normal
    
  if(FLAG_APC_presente == true){
    Serial.print(F("APC_OK"));
  }
  else{
    Serial.print(F("APC_FAIL"));
  }
  Serial.write(0x0D);            // fin de linea
  Serial.write(0x0A);

}


//========================================================
// LEER CONFIGURACION ACTUAL DEL APC220
//========================================================

void read_config() 
{
  digitalWrite(SET, LOW);         // poner en modo configuracion
  delay(50);                      // pausa para estabilizar 50
  APCport.print("RD");            // peticion de datos
  APCport.write(0x0D);            // fin de linea
  APCport.write(0x0A);            // y retorno de carro. Similar a hacer un 'println', pero con println no funciona :(
  delay(200);                     // pausa para estabilizar 200

  bool FLAG_APC_presente = false;
  while (APCport.available()) {
    FLAG_APC_presente = true;
    Serial.write(APCport.read()); 
  }
  
  if(FLAG_APC_presente == false){
    Serial.print(F("APC_FAIL"));
  }
  
  Serial.write(0x0D);            // fin de linea
  Serial.write(0x0A);
  
  digitalWrite(SET, HIGH);        // volver al modo normal
}


//========================================================
// ESCRIBIR NUEVA CONFIGURACION EN EL APC220
//========================================================

void write_config(String nueva_configuracion)
{
  digitalWrite(SET, LOW);               // poner en modo configuracion
  delay(50);
  APCport.print(nueva_configuracion);   // consultar el datasheet para detalle de los parametros
  APCport.write(0x0D);                  // fin de linea
  APCport.write(0x0A);                  // y retorno de carro. Similar a hacer un 'println', pero con println no funciona :(
  delay(100);
  digitalWrite(SET, HIGH);              // volver al modo normal
}



//*******************************************************
//                    FIN DE PROGRAMA
//*******************************************************
