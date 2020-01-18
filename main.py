from subNats import *

posList = list()

def dataReadyCallback(dataPoint):
    posList.append(dataPoint)

initPosCollection(dataReadyCallback)
