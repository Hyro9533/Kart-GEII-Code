""" 
Made by MONTGUILLON Jonathan - BUT3 GEII
For IUT Of Chartres
2023-10
"""

#include "./myLibIno/module_lora.h"

const uint8_t pData[] = {0xCA};
uint16_t len = 1; // Update the length to match the data length


CModuleLoRa* pModuleLoRa = CModuleLoRa::GetInstance();

void setup() {

  erial.begin(9600);

  
  pModuleLoRa->init(10, 0, 1);
  

  // Print module configuration to Serial
  pModuleLoRa->setConfig();
  
}

void loop() {

  //Si envoie du stand rajouter 1s de délay

  pData --> Capteur de Maxime(AnalogRead)

  int lenOfArray = 11

  char data[lenOfArray] = {
    "temp1", // ???? SPI MODE 
    "temp2", // ???? SPI MODE 
    "temp3", // ???? SPI MODE
    Capteur_DE_Maxime(A1), // Sensor : Acceleration
    Capteur_DE_Maxime(A0), // Sensor : Brake
    Capteur_DE_Maxime(A6), // Sensor : TensionBB
    Capteur_DE_Maxime(A7), // Sensor : Tension SB 
    Capteur_DE_Maxime(A3), // Sensor : Current
    Capteur_DE_Maxime(D11), // Sensor : Speed
    {                 // Sensor : GPS
      Capteur_DE_Maxime(D0),
      Capteur_DE_Maxime(D1)
    },
    0,
  };

  for(int i = 0; i <= lenOfArray; i++) {
    Serial.println(data[i]);
  };


  pModuleLoRa->radioTX(data, len);

  

  delay(1000);


}


