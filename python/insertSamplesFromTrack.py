import sys
import random
import calendar
from config import *

# This is very slow implementation. It takes about 10 minutes to fill in one month
# TODO read whole track into the memory and then fill sensor table from it

def save_to_db(sensorid, sensed):

    last = "SELECT lastid FROM sensor_id" + str(sensorid) + " ORDER BY sensed DESC LIMIT 1"
    mycursor = mydb.cursor()
    mycursor.execute(last)
    records = mycursor.fetchall()

    idtoget = 1
    if len(records) > 0:
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
    ins = "INSERT INTO sensor_id" + str(sensorid) + " (distance_error, measure, sensed, lon, lat, lastid) VALUES (" + str(distance) + ", " + str(measured) + ", '" + str(sensed) + "', " + str(records[0][0]) + ", " + str(records[0][1]) + ", " + str(idtoget) + ")"
    # print(ins)
    mycursor3.execute(ins)
    mydb.commit()

if len(sys.argv) < 3:
    print("Usage: python3 insertSamplesFromTrack.py sensorid month")
    print("Example: python3 insertSamplesFromTrack.py 1 1")
    exit(1)

mydb = getConnection()

maxday = calendar.monthrange(2020, int(sys.argv[2]))[1]

for k in range(maxday):
    for j in range(24):
        for i in range(60):
            min = i
            if i < 10:
                min = "0" + str(i)
            hour = j
            if j < 10:
                hour = "0" + str(j)
            day = k+1
            if k < 9:
                day = "0" + str(k+1)
            val3 = '2020-' + sys.argv[2] + '-' + str(day) + ' ' + str(hour) + ':' + str(min) + ':01'
            save_to_db(sys.argv[1], val3)