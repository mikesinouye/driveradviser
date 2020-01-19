from subNats import *
from pathPrediction import *
from python.car_modeling.Car import *
import sys

x = int(sys.argv[1])

ownPredictor = PathPredictor()
target1Predictor = PathPredictor()
target2Predictor = PathPredictor()
target3Predictor = PathPredictor()

def dataReadyCallback(dataPoint):
    if(dataPoint.positionModel.OwnPosition != 0.0):
        ownPredictor.hasPosData = True
        ownPredictor.addData(dataPoint.positionModel.OwnPosition, dataPoint.timestamp)
    else:
        ownPredictor.hasPosData = False
    if(dataPoint.positionModel.Target1Position != 0.0):
        target1Predictor.hasPosData = True
        target1Predictor.addData(dataPoint.positionModel.Target1Position, dataPoint.timestamp)
    else:
        target1Predictor.hasPosData = False
    if(dataPoint.positionModel.Target2Position != 0.0):
        target2Predictor.hasPosData = True
        target2Predictor.addData(dataPoint.positionModel.Target2Position, dataPoint.timestamp)
    else:
        target2Predictor.hasPosData = False
    if(dataPoint.positionModel.Target3Position != 0.0):
        target3Predictor.hasPosData = True
        target3Predictor.addData(dataPoint.positionModel.Target3Position, dataPoint.timestamp)
    else:
        target3Predictor.hasPosData = False

    if(ownPredictor.hasPosData):
        if(target1Predictor.hasPosData):
            Car.predict_collision(ownPredictor.latestCar, target1Predictor.latestCar)
        if(target2Predictor.hasPosData):
            Car.predict_collision(ownPredictor.latestCar, target2Predictor.latestCar)
        if(target3Predictor.hasPosData):
            Car.predict_collision(ownPredictor.latestCar, target3Predictor.latestCar)

if __name__ == "__main__":
    initPosCollection(dataReadyCallback, x)