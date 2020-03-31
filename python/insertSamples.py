# CREATE USER '*'@'localhost' IDENTIFIED BY '*';
# mycursor.execute("CREATE TABLE sensor_id1 (id SERIAL, distance_error FLOAT, measure FLOAT, sensed DATETIME DEFAULT NOW())")

import sys
import random
import calendar
from config import *

if len(sys.argv) < 3:
  print("Usage: python3 insertSamples.py sensorid month")
  print("Example: python3 insertSamples.py 1 1")
  exit(1)

mydb = getConnection()
mycursor = mydb.cursor()
maxday = calendar.monthrange(2020, int(sys.argv[2]))[1]

for k in range(maxday):
  for j in range(24):
    for i in range(60):
      val1 = (random.random() * 300) + 20
      val2 = (random.random() * 30) + 5
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
      ins = "INSERT INTO sensor_id" + sys.argv[1] + " (distance_error, measure, sensed) VALUES (" + str(val1) + ", " + str(val2) + ", '" + val3 + "')"
      mycursor.execute(ins)
      # print(ins)

mydb.commit()
