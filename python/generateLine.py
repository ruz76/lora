from datetime import datetime
import random
import sys

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%Y-%m-%dT%H:%M:%S")

gtws = ['eui-b827ebfffe998292',
        'eui-b827ebfffe411ace',
        'eui-b827ebfffe13b290',
        'eui-b827ebfffe71f386']

ms = [[125300, 125300, 125300, 125300], [125310, 125300, 125290, 125305]]

sensorid = int(sys.argv[1])

line = ''
for i in range(len(gtws)):
    # random error
    diff = random.randint(1, 50)
    # diff = 0
    line += gtws[i] + ";" + dt_string + "." + str(ms[sensorid][i] + diff) + "Z&"

print(line)
# print('eui-b827ebfffe998292;2020-02-06T16:03:40.001312Z&eui-b827ebfffed3b23f;&eui-b827ebfffe411ace;2020-02-06T16:03:40.001312Z&eui-b827ebfffe13b290;2020-02-06T16:03:40.001312Z&eui-b827ebfffe71f386;2020-02-06T16:03:40.001312Z')