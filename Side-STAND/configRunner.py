""" 
--Program--
Credit : Made by MONTGUILLON Jonathan - BUT3 GEII
Client : IUT Of Chartres
Date : 2023-10
"""

##Need to be changed !
ArchivesConfig = {
  "pathOfArchives" : "/Users/jonathanmontguillon/Library/CloudStorage/OneDrive-Universitéd'Orléans/IUT/BUT 3/SAE/Projet - Kart/Project-Code/Kart-GEII-Code/Side-STAND/Data",

  "limitOfArchives" : 10000
}

#MySQL Connection

MySQL = { 
  "user" : "root",
  "password" : "zphypry20031672",
  "host" : "localhost",
  "database" : "DATA_KART_GEII"
}


#Data Constant
import random

dataConstant = {
  
  "listOfSensors" : [
    #String Value for every one, but maybe arrayValue for GPS.
    "temp1", 
    "temp2",
    "temp3",
    "temp4",
    "temp5",
    "acceleration",
    "brake",
    "tensionBB", #BB --> Big Batterie - Charge at 48V, unload at 44V.
    "tensionSB", #SB --> Small Batterie - Charge at 12V, unload at 11V.
    "current",
    "speed",
    "GPS", #Need to be talking, we have to send an array of 2 values ?
    "time", #TimeStamp there, be carrefull ! GPS
  ],
  #Returning this sort of array : [ "1", "2", "3", "4", "5", "6", "7", "8", "9", [ "1", "2" ], "10"

  "dataOfSensors" : [
    round(random.uniform(1.0, 199.99), 2), #Temp1 - 0
    round(random.uniform(1.0, 199.99), 2), #Temp2 - 1
    round(random.uniform(1.0, 199.99), 2), #Temp3 - 2
    round(random.uniform(1.0, 199.99), 2), #Temp4 - 3
    round(random.uniform(1.0, 199.99), 2), #Temp5 - 4
    round(random.uniform(0.0, 99.99), 2),  #Acceleration - 5
    round(random.uniform(0.0, 99.99), 2),  #Brake - 6
    round(random.uniform(11.0, 12.9), 1),  #TensionBB - 7
    round(random.uniform(44.0, 48.9), 1),  #TensionSB - 8
    round(random.uniform(0.0, 399.9), 1),  #Current - 9
    round(random.uniform(0, 99), 0),       #Speed - 10
    [ round(random.uniform( (-999.9999), 999.9999),4), round(random.uniform( (-999.9999), 999.9999),4)],   #GPS - 11
    round(random.uniform(10000000000, 19999999999),8), #Time - 12
  ]
  
}
 
#Query for User
def typeOfDataRunning():
  print("\n\n\nVoulez-vous une acquisition Physique ou Virtuelle ? ")
  print("Physique (Via Lora) --> 1")
  print("Virtuelle (Génération de Valeurs) --> 2")
  print("\nValeur à entrez : ")
  
  return int(input())
  
  