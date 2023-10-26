""" 
--Program--
Credit : Made by MONTGUILLON Jonathan - BUT3 GEII
Client : IUT Of Chartres
Date : 2023-10
"""

#######################################################################

#All Librairies
import json
import os

from datetime import datetime

import random


#######################################################################

#######################################################################

""" 
Client Need to Change Things there !
"""

#This two variables need to be absolutly check by the client to be sure that the path and the fileName, and promptly corresponding to the machine (Server)
fileNameGlobal = "data.json"
#pathNameGlobal = "C:/Users/jonat/OneDrive - Université d'Orléans/IUT/BUT 3/SAE/Projet - Kart/Code Python/" + fileNameGlobal
pathNameGlobal = "/Users/jonathanmontguillon/Library/CloudStorage/OneDrive-Universitéd'Orléans/IUT/BUT 3/SAE/Projet - Kart/Code Python/" + fileNameGlobal

#######################################################################

#######################################################################

""" 
Client Need to Change Things there !
"""

#This variable have to be according with the several pin of sensors, that you need. ("AnalogRead" and "DigitalRead" for Arduino)

#So for the receiver, you have to put lora.rx()

arrayAllValuesOfSensorsFromArduinoPins = [
  round(random.uniform(1.0, 199.99), 2),
  round(random.uniform(1.0, 199.99), 2), 
  round(random.uniform(1.0, 199.99), 2), 
  round(random.uniform(0.0, 99.99), 2), 
  round(random.uniform(0.0, 99.99), 2),
  round(random.uniform(11.0, 12.9), 1),
  round(random.uniform(44.0, 48.9), 1), 
  round(random.uniform(0.0, 399.9), 1), 
  round(random.uniform(0, 99), 0), 
  [ round(random.uniform( (-999.9999), 999.9999),4), round(random.uniform( (-999.9999), 999.9999),4)],
  round(random.uniform(10000000000, 19999999999),8),
]

listOfSensors = [
  #String Value for every one, but maybe arrayValue for GPS.
  "temp1", 
  "temp2",
  "temp3",
  "acceleration",
  "brake",
  "tensionBB", #BB --> Big Batterie - Charge at 48V, unload at 44V.
  "tensionSB", #SB --> Small Batterie - Charge at 12V, unload at 11V.
  "current",
  "speed",
  "GPS", #Need to be talking, we have to send an array of 2 values ?
  "time", #TimeStamp there, be carrefull ! GPS
]

#######################################################################

#Functions For JSON Formatting
#Please do not touch everything there !

def writeInFile(fileName, pathFile, dataForFile):

  dataInLocal = []

  try :
    with open(pathFile, "r") as r:

      try :
        
        dataInLocal = json.load(r)

      except:

        print("File Empty")
  
  except:
    createFileJSON(fileName,pathFile)
    
  with open(pathFile,"w") as f:

    try: 
      
      dataEmptyForPurge = []

      json.dump(dataEmptyForPurge, f)

    except:

      print("Cannot Write Purge in file")

  dataInLocal.append(dataForFile)
  
  with open(pathFile,"w") as f:

    try: 
      
      json.dump(dataInLocal, f, indent = 4, separators=(',', ': '), sort_keys = True)

    except:

      print("Cannot Write DATA in file")

    
  return True


def getLineOfObjectInFile(fileName, pathFile):

  dataInFile = []
  numberOfObjets = 0

  try:
    
    with open(pathFile, "r") as r:

      dataInFile = json.load(r)

      numberOfObjets = len(dataInFile)

  except:

    print("Problem to Read File for GetLineOfOBjectInFile")

  return int(numberOfObjets)

def getLineOfFile(fileName, pathFile):

  numberOfFile = 0

  try:

    with open(pathFile, "r") as r:

      for line in r:
        numberOfFile +=1

  except :

    print("Problem to Read File for GetLineOfFile")

  return int(numberOfFile)

def verifySizeOfFile(fileName, pathFile, sizeLimitOfLine):

  counterOfLine = getLineOfFile(fileName,pathFile)

  if(counterOfLine >= sizeLimitOfLine):

    changeNameOfFile(pathFile, fileName, createFileNameForArchive() )

    createFileJSON(fileName, pathFile)

    return True

  else:
    return False

def createFileNameForArchive():
  CurrentTime = datetime.now()

  CurrentTimeFormated = CurrentTime.strftime("_%d-%m-%Y_%HH%M'%S")

  nameForArchive = "Archives-KART" + str(CurrentTimeFormated)

  return nameForArchive

def changeNameOfFile(oldEntirePathFile, oldNameFile, newNameFile):

  try :
    newFolder = "Archives/"
    extensionFile = ".json"

    oldFileName = oldEntirePathFile.split(oldNameFile)[0]
    newFileName = oldFileName + newFolder + newNameFile + extensionFile
    
    os.rename(oldEntirePathFile, newFileName)

    fileNameGlobal = newNameFile

    return True

  except:

    return False

def createFileJSON(fileName, pathFile):

  try:

    dataEmptyCreatedFile = []

    with open(pathFile, "w") as f:

      json.dump(dataEmptyCreatedFile, f)

      return True

  except:

    return False

#######################################################################

#######################################################################

#Create Dict Array to merge in JSON.

def createDataForFile(fileName,pathFile,arrayOfKeys, arrayOfValues):

  dataOfJSONForValues = {}

  value=0

  for key in arrayOfKeys:
    
    dataOfJSONForValues[key] = arrayOfValues[value]

    value +=1

  dataJSON = {}
  dataJSONFormat = {}

  dataJSONFormat["Value(s)"] = dataOfJSONForValues
  dataJSON[getLineOfObjectInFile(fileName,pathFile) + 1] = dataJSONFormat

  #print(dataJSON) 

  return dataJSON

#######################################################################

#######################################################################

#Debug for Calling Functions

#Calling Function ChangeFileName : 
# 
# print("Changing Name of file : ",changeNameOfFile(pathNameGlobal, fileName, "NewNameData"))


#Calling Function VerifySize Of File :
#
#print("Purge File : ", verifySizeOfFile(fileNameGlobal, pathNameGlobal, 100))



#Calling Function to Create File :
#
#print(createFileJSON(fileNameGlobal, pathNameGlobal))


#Calling Function to get Number of Objets in file :
#
#print(getLineOfObjectInFile(fileNameGlobal,pathNameGlobal))

#Calling Function to get Number Of Line in file : 
#
#print(getLineOfFile(fileNameGlobal,pathNameGlobal))

#######################################################################

#######################################################################

#Run Main Program from functions built-in
#
#
def RunnerForArchives(dataFromKart, sensorsFromKart, pathOfFolder, limitOfLineInFileForArchive):
  
  pathOfFolder = pathOfFolder + "/" + fileNameGlobal

  #While TRUE
  dataFormatedForJSON = createDataForFile(fileNameGlobal,pathOfFolder,sensorsFromKart,dataFromKart)
  writeInFile(fileNameGlobal, pathOfFolder, dataFormatedForJSON)

  verifySizeOfFile(fileNameGlobal, pathOfFolder, limitOfLineInFileForArchive)
  
  return dataFormatedForJSON


#######################################################################

