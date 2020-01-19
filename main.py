from subNats import *
from pathPrediction import *

#posList = list()

ownPredictor = PathPredictor()
target1Predictor = PathPredictor()
target2Predictor = PathPredictor()
target3Predictor = PathPredictor()

def dataReadyCallback(dataPoint):
    #posList.append(dataPoint)
    if(dataPoint.positionModel.State.OwnPosition != None):
        ownPredictor.hasPosData = True
        pathPredictor.addData(dataPoint.positionModel.State.OwnPosition, dataPoint.timestamp)
    else:
        ownPredictor.hasPosData = False
    if(dataPoint.positionModel.State.Target1Position != None):
        target1Predictor.hasPosData = True
        pathPredictor.addData(dataPoint.positionModel.State.Target1Position, dataPoint.timestamp)
    else:
        target1Predictor.hasPosData = False
    if(dataPoint.positionModel.State.Target2Position != None):
        target2Predictor.hasPosData = True
        pathPredictor.addData(dataPoint.positionModel.State.Target2Position, dataPoint.timestamp)
    else:
        target2Predictor.hasPosData = False
    if(dataPoint.positionModel.State.Target3Position != None):
        target3Predictor.hasPosData = True
        pathPredictor.addData(dataPoint.positionModel.State.Target3Position, dataPoint.timestamp)
    else:
        target3Predictor.hasPosData = False

    if(ownPredictor.hasPosData):
        if(target1Predictor.hasPosData):
            Car.predict_collisions(ownPredictor.latestCar, target1Predictor.latestCar)
        if(target2Predictor.hasPosData):
            Car.predict_collisions(ownPredictor.latestCar, target2Predictor.latestCar)
        if(target3Predictor.hasPosData):
            Car.predict_collisions(ownPredictor.latestCar, target3Predictor.latestCar)

if __name__ == "__main__":
    initPosCollection(dataReadyCallback)