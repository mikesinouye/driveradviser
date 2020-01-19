import sys
import json

file = open("../data/stream.txt", "r")
lines = file.readlines()
linenum = 16 * int(sys.argv[1])

OwnLat = lines[linenum + 1].strip()
OwnLong = lines[linenum + 2].strip()
OwnHead = lines[linenum + 4].strip()

Target1Lat = lines[linenum + 8].strip()
Target1Long = lines[linenum + 9].strip()
Target1Head = lines[linenum + 11].strip()

data = "{ \"OwnLat\":\"" + OwnLat + "\", " + "\"OwnLong\":\"" + OwnLong + "\", " + "\"OwnHead\":\"" + OwnHead + "\", " + "\"Target1Lat\":\"" + Target1Lat + "\", " + "\"Target1Long\":\"" + Target1Long + "\", " + "\"Target1Head\":\"" + Target1Head + "\"}"
print(data)
sys.stdout.flush()