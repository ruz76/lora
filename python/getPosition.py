import math
import datetime
import sys

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

    cellsize = 10
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

    print(bestx, besty)
    return bestx, besty


# gtws = {'eui-b827ebfffe998292': [0, 0],
#         'eui-b827ebfffed3b23f': [5000, 5000],
#         'eui-b827ebfffe411ace': [10000, 0],
#         'eui-b827ebfffe13b290': [10000, 10000],
#         'eui-b827ebfffe71f386': [0, 10000]}

gtws = {'eui-b827ebfffe998292': [4906688, 3001349],
        'eui-b827ebfffed3b23f': [4906252, 2995691],
        'eui-b827ebfffe411ace': [4906867, 3001407],
        'eui-b827ebfffe13b290': [4914903, 3004002],
        'eui-b827ebfffe71f386': [4913906, 2995884]}

line = sys.argv[1]
# line = 'eui-b827ebfffe998292;2020-02-06T16:03:40.001312Z&eui-b827ebfffed3b23f;&eui-b827ebfffe411ace;2020-02-06T16:03:42.000112Z&eui-b827ebfffe13b290;2020-02-06T16:03:39.00005Z&eui-b827ebfffe71f386;2020-02-06T16:03:39.00007Z'
# line = 'eui-b827ebfffe998292;2020-02-06T16:03:40.001312Z&eui-b827ebfffed3b23f;&eui-b827ebfffe411ace;2020-02-06T16:03:40.001312Z&eui-b827ebfffe13b290;2020-02-06T16:03:40.001312Z&eui-b827ebfffe71f386;2020-02-06T16:03:40.001312Z'
gtts = get_current_gtts(line)
get_position(gtws, gtts)
#print(gtts)