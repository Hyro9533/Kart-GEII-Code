""" 
Project : KART GEII (FROM "SAE")
Project Owner : M. Ducornetz Timothé
Supervisor : M. Bruno Sohier

--Program--
Credit : Made by MONTGUILLON Jonathan - BUT3 GEII
Client : IUT Of Chartres
Date : 2023-10

Contact : montguillonjonathan@gmail.com

Enjoy !
"""

##Library Local
from myLibPy.JSON_Archives import RunnerForArchives
from myLibPy.LORA_Configuration import LoRa_RN2483
from myLibPy.MySQL_Configuration import mergedIntoMySQLForRX
from myLibPy.MySQL_Configuration import mergedIntoMySQLForTX

import configRunner #Keys for MONTGUILLON


##Installing Package 

#pip3 install mysql
#pip3 install pyserial



##
LOOP = True #Acquisiton Automaticly set



while LOOP == True:
  
  print("Loop Program for RX")
  
  #Acquisiton OF DATA
  DEBUG_Acquisition = 2 ## SWITCH TO 0 WHEN THE DVP HAS ENEDED

  while (DEBUG_Acquisition != 2) and (DEBUG_Acquisition != 1):
    
    DEBUG_Acquisition = configRunner.typeOfDataRunning()


  listOfSensorsAccordingWithData = configRunner.dataConstant["listOfSensors"]

  if(DEBUG_Acquisition == 2):
    
    dataFromKart = configRunner.dataConstant["dataOfSensors"]
    
  else:
    
    LoraConnectionWireless = lora_RN2483.LoRa_RN2483()

    LoraConnectionWireless.config()
    dataFromKart = LoraConnectionWireless.rx()
    
    print("Encodage à modifier ICI ???????", dataFromKart)
  ##



  #Archiving of DATA
  pathOfArchivesFolder = configRunner.ArchivesConfig["pathOfArchives"]
  limitOfLineInFileForArchive = configRunner.ArchivesConfig["limitOfArchives"]

  jsonFormated = RunnerForArchives(dataFromKart, listOfSensorsAccordingWithData, pathOfArchivesFolder, limitOfLineInFileForArchive)
  ##
  
  #Put in MySQL
 
  mergedIntoMySQLForRX(configRunner.MySQL,dataFromKart, listOfSensorsAccordingWithData, jsonFormated)
  ##
  
  
  
  
  
  
  
  
  print("Loop Program for TX")
  #To Code !
  
  
  
  print("END OF LOOP, DELAY NEEDABLE ?")
  LOOP = False
  