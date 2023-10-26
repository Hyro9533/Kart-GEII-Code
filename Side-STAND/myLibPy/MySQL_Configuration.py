""" 
--Program--
Credit : Made by MONTGUILLON Jonathan - BUT3 GEII
Client : IUT Of Chartres
Date : 2023-10
"""

import mysql.connector
import json
#
MySQL = { 
  "user" : "root",
  "password" : "zphypry20031672",
  "host" : "localhost",
  "database" : "DATA_KART_GEII"
}

def testConnexionToDataBase(configDB):
  
  try: 
    connectionText = mysql.connector.connect(configDB)
    
    connectionText.cursor()
    
    connectionText.close()
    
  except:
    
    createDatabase(configDB)

def createDatabase(configDB):
  
  try :
    
    mydb = mysql.connector.connect(
      host= configDB["host"],
      user= configDB["user"],
      password= configDB["password"]
    )

    mycursor = mydb.cursor()

    requete_CREATE_Database = "CREATE DATABASE IF NOT EXISTS DATA_KART_GEII"
    mycursor.execute(requete_CREATE_Database)

    mycursor.close()
  except:
    
    print("Base de Données MySQL OUT : Time OUT !")

class dataBaseMySQL:
  
  def __init__(self, configDB):
    
    self.connexionDB = mysql.connector.connect(**configDB)
    self.curseur = self.connexionDB.cursor()
    
  def createTable(self, sqlRequest, sqlParam):
    
    self.executeSQL(sqlRequest, sqlParam)
    self.validate()
    
  def insertIntoTable(self, sqlRequest, sqlParam):
    
    self.executeSQL(sqlRequest, sqlParam)
    self.validate()

  def executeSQL(self, sqlRequest, sqlParam):
    
 
    try:
        if sqlParam:
    
            self.curseur.execute(sqlRequest, sqlParam)
        else:
            self.curseur.execute(sqlRequest)
    except Exception as err:
        # afficher le message d'erreur système
        print("\nErreur détectée :")
        print(err)
        return 0
    else:
        # afficher l'exécution réussie de la requête
        print("\nRequête exécutée")
        return 1
    
  def validate(self):
    
    if self.connexionDB:
      self.connexionDB.commit()
      
  def close(self):
    
    if self.connexionDB != None:
      self.connexionDB.close()


def mergedIntoMySQLForRX(configDB, values, keys, JSONBrut):
  testConnexionToDataBase(configDB)
  
  DBMySQL = dataBaseMySQL(configDB)
  
  requete_CREATE_TableRX = "CREATE TABLE IF NOT EXISTS DATA_RX ( \
      id int primary key auto_increment,\
      temp1 CHAR(30),\
      temp2 CHAR(30),\
      temp3 CHAR(30),\
      acceleration CHAR(30),\
      brake CHAR(30),\
      tensionBB CHAR(30),\
      tensionSB CHAR(30),\
      current CHAR(30),\
      speed CHAR(30),\
      GPS JSON, \
      time CHAR(30), \
      RX bool default FALSE,\
      TX bool default FALSE,\
      Archives_BRUT_Values JSON\
  )"

  DBMySQL.createTable(requete_CREATE_TableRX, None )
  
  requete_INSERT_TableRX = "INSERT INTO DATA_RX (temp1, temp2, temp3, acceleration, brake, tensionBB, tensionSB, current, speed, GPS, time, RX, TX, Archives_BRUT_Values) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  
  
  dictForGPS = { "Longitutde" : str(values[9][0]), "Latitude" : str(values[9][1])}
  
  DBMySQL.insertIntoTable(requete_INSERT_TableRX, (values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], json.dumps(dictForGPS, indent=4), values[10], 1, 0, json.dumps(JSONBrut, indent=4) ) )
  
  DBMySQL.close()


def mergedIntoMySQLForTX(configDB, values, keys, JSONBrut):
  testConnexionToDataBase(configDB)
  
  DBMySQL = dataBaseMySQL(configDB)
  
  requete_CREATE_TableTX = "CREATE TABLE IF NOT EXISTS DATA_TX ( \
      id int primary key auto_increment,\
      alert_Maintenance int default 0,\
      start_Chrono bool default FALSE,\
      stop_Chrono bool default FALSE,\
      time date not null, \
      RX bool default FALSE,\
      TX bool default FALSE\
  )"
  MySQL.createTable(requete_CREATE_TableTX, None)
  
  #To Code There, send value when the alert_Maintenance is HIGH !
  # SELECT --> CHECK-LOCAL --> UPDATE
  
  DBMySQL.close()
  


