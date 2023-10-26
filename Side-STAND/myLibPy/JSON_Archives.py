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

fileNameGlobal = "data.json"



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


def RunnerForArchives(dataFromKart, sensorsFromKart, pathOfFolder, limitOfLineInFileForArchive):
  
  pathOfFolder = pathOfFolder + "/" + fileNameGlobal

  #While TRUE
  dataFormatedForJSON = createDataForFile(fileNameGlobal,pathOfFolder,sensorsFromKart,dataFromKart)
  writeInFile(fileNameGlobal, pathOfFolder, dataFormatedForJSON)

  verifySizeOfFile(fileNameGlobal, pathOfFolder, limitOfLineInFileForArchive)
  
  return dataFormatedForJSON


#######################################################################

