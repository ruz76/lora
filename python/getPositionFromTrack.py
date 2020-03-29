import math
import datetime
import sys
import mysql.connector
import random
from config import *

def save_to_db(sensorid):

    last = "SELECT lastid FROM sensor_id" + str(sensorid) + " ORDER BY sensed DESC LIMIT 1"
    mycursor = mydb.cursor()
    mycursor.execute(last)
    records = mycursor.fetchall()

    idtoget = records[0][0] + 1
    if idtoget == 814:
        idtoget = 1

    coords = "SELECT lon, lat FROM track WHERE id = " + str(idtoget)
    mycursor2 = mydb.cursor()
    mycursor2.execute(coords)
    records = mycursor2.fetchall()

    measured = (random.random() * 30) + 5
    distance = (random.random() * 300) + 10

    mycursor3 = mydb.cursor()
    ins = "INSERT INTO sensor_id" + str(sensorid) + " (distance_error, measure, sensed, lon, lat, lastid) VALUES (" + str(distance) + ", " + str(measured) + ", NOW(), " + str(records[0][0]) + ", " + str(records[0][1]) + ", " + str(idtoget) + ")"
    mycursor3.execute(ins)
    mydb.commit()


mydb = getConnection()


sensorid = int(sys.argv[1])
save_to_db(sensorid)