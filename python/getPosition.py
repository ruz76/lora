import math
import datetime
import sys
import mysql.connector
import random
from config import *

def gt(dt_str):
    """Converts UTC date string to date."""

    dt, _, us = dt_str.partition(".")
    dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    us = int(us.rstrip("Z"), 10)
    return dt + datetime.timedelta(microseconds=us)

def get_extent(gtws):
    """Returns extent of gateways (parameter gtws)."""

    minx = float("inf")
    miny = float("inf")
    maxx = float("-inf")
    maxy = float("-inf")

    for gtw in gtws:
        if gtws[gtw][0] < minx:
            minx = gtws[gtw][0]
        if gtws[gtw][0] > maxx:
            maxx = gtws[gtw][0]
        if gtws[gtw][1] < miny:
            miny = gtws[gtw][1]
        if gtws[gtw][1] > maxy:
            maxy = gtws[gtw][1]

    print (minx, miny, maxx, maxy)
    return minx, miny, maxx, maxy


def get_current_gtts(line):
    """Returns dictionary of gateways and their timestamps in date format."""

    gtts = {}
    items = line.split('&')
    for i in range(len(items)):
        fields = items[i].split(';')
        if len(fields) > 1:
            if fields[1] != '':
                gtts[fields[0]] = gt(fields[1])

    gtts = sorted(gtts.items(), key=lambda x: x[1])
    firstdate = gtts[0][1]
    gtts_out = {}
    for gttsx in gtts:
        if ((gttsx[1]-firstdate) > datetime.timedelta(seconds=0.5)):
            while (gttsx[1]-firstdate) > datetime.timedelta(seconds=0.5):
                gttsx = (gttsx[0], gttsx[1] - datetime.timedelta(seconds=0.5))
            print(gttsx[1]-firstdate)
        gtts_out[gttsx[0]] = gttsx[1]-firstdate+datetime.timedelta(seconds=0.0001)

    return gtts_out


def get_position(gtws, gtts):
    """Returns best suiting pixel according to timestamps (gtts)
    and positions of gateways (gtws)."""

    minx, miny, maxx, maxy = get_extent(gtws)

    cellsize = 50
    rows = int((maxy - miny) / cellsize) + 1  # +1 to cover whole area
    cols = int((maxx - minx) / cellsize) + 1  # +1 to cover whole area

    difference = float("inf")
    bestx = 0
    besty = 0
    for row in range(rows):
        for col in range(cols):
            currentx = minx + (row * cellsize)
            currenty = miny + (col * cellsize)

            distances = {}
            for gtw in gtws:
                distances[gtw] = math.hypot(currentx - gtws[gtw][0], currenty - gtws[gtw][1])

            differences = {}
            for gtt in gtts:
                differences[gtt] = abs(distances[gtt] / gtts[gtt].microseconds)

            current_difference = 0
            for gtt1 in gtts:
                for gtt2 in gtts:
                    current_difference += abs(differences[gtt1] - differences[gtt2])

            if (current_difference < difference):
                bestx = currentx + (cellsize / 2)
                besty = currenty + (cellsize / 2)
                difference = current_difference

    return bestx, besty

def save_to_db(sensorid, coords_fixed, coords_fixed_wgs, coords_computed):

    distance = math.hypot(coords_fixed[0] - coords_computed[0], coords_fixed[1] - coords_computed[1])

    measured = (random.random() * 30) + 5

    mycursor = mydb.cursor()
    ins = "INSERT INTO sensor_id" + str(sensorid) + " (distance_error, measure, sensed, lon, lat) VALUES (" + str(distance) + ", " + str(measured) + ", NOW(), " + str(coords_fixed_wgs[0]) + ", " + str(coords_fixed_wgs[1]) + ")"
    mycursor.execute(ins)
    mydb.commit()

def getSensor(sensorid):

    last = "SELECT x, y, lon, lat FROM sensors WHERE id = " + str(sensorid)
    mycursor = mydb.cursor()
    mycursor.execute(last)
    records = mycursor.fetchall()
    return records[0][0], records[0][1], records[0][2], records[0][3]

def getGtws():
    gtws = {}
    last = "SELECT mqttid, x, y FROM gtws"
    mycursor = mydb.cursor()
    mycursor.execute(last)
    records = mycursor.fetchall()
    for row in records:
        gtws.update( {row[0] : [row[1], row[2]]} )

    return gtws

mydb = getConnection()


# gtws = {'eui-b827ebfffe998292': [4906688, 3001349],
#         'eui-b827ebfffed3b23f': [4906252, 2995691],
#         'eui-b827ebfffe411ace': [4906867, 3001407],
#         'eui-b827ebfffe13b290': [4914903, 3004002],
#         'eui-b827ebfffe71f386': [4913906, 2995884]}

gtws = getGtws()

line = sys.argv[1]
# line = 'eui-b827ebfffe998292;2020-02-06T16:03:40.001312Z&eui-b827ebfffed3b23f;&eui-b827ebfffe411ace;2020-02-06T16:03:42.000112Z&eui-b827ebfffe13b290;2020-02-06T16:03:39.00005Z&eui-b827ebfffe71f386;2020-02-06T16:03:39.00007Z'
# line = 'eui-b827ebfffe998292;2020-02-06T16:03:40.001312Z&eui-b827ebfffed3b23f;&eui-b827ebfffe411ace;2020-02-06T16:03:40.001312Z&eui-b827ebfffe13b290;2020-02-06T16:03:40.001312Z&eui-b827ebfffe71f386;2020-02-06T16:03:40.001312Z'
gtts = get_current_gtts(line)
# print(gtts)
x, y = get_position(gtws, gtts)
# print(x, y)

sensorid = int(sys.argv[2])
# sensors = [[4911627, 3000316], [4911977, 3000666]]
# sensors_wgs = [[18.22554, 49.81724], [18.23091, 49.82001]]
sx, sy, slon, slat = getSensor(sensorid + 1)
save_to_db(sensorid + 1, [sx, sy], [slon, slat], [x, y])