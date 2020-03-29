# CREATE USER '*'@'localhost' IDENTIFIED BY '*';
# mycursor.execute("CREATE TABLE sensor_id1 (id SERIAL, distance_error FLOAT, measure FLOAT, sensed DATETIME DEFAULT NOW())")

import mysql.connector
import random

mydb = mysql.connector.connect(
  host="127.0.0.1",
  port="3306",
  database="*",
  user="*",
  passwd="*"
)

for k in range(30):
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
      val3 = '2020-01-' + str(day) + ' ' + str(hour) + ':' + str(min) + ':01'
      ins = "INSERT INTO sensor_id2 (distance_error, measure, sensed) VALUES (" + str(val1) + ", " + str(val2) + ", '" + val3 + "')"
      mycursor.execute(ins)
      #print(ins)

mydb.commit()
