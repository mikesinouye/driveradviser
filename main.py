from subNats import *
from pathPrediction import *
from python.car_modeling.Car import *
import sys

x = -1
if len(sys.argv) > 1:
    x = int(sys.argv[1])
else:
    x = 0

ownPredictor = PathPredictor()
target1Predictor = PathPredictor()
target2Predictor = PathPredictor()
target3Predictor = PathPredictor()

def dataReadyCallback(dataPoint):
    return_list = []
    alert_list = []
    #collect data
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
    #calc collisions and
    if(ownPredictor.hasPosData and ownPredictor.latestCar != None):
        return_list.append(ownPredictor.predictPath(8, 4))
        if(target1Predictor.hasPosData and target1Predictor.latestCar != None):
            alert_list.append(Car.predict_collision_lin(ownPredictor.latestCar, target1Predictor.latestCar))
            return_list.append(target1Predictor.predictPath(8, 4))
        if(target2Predictor.hasPosData and target2Predictor.latestCar != None):
            alert_list.append(Car.predict_collision_lin(ownPredictor.latestCar, target2Predictor.latestCar))
            return_list.append(target2Predictor.predictPath(8, 4))
        if(target3Predictor.hasPosData and target3Predictor.latestCar != None):
            alert_list.append(Car.predict_collision_lin(ownPredictor.latestCar, target3Predictor.latestCar))
            return_list.append(target3Predictor.predictPath(8, 4))

    return (return_list, alert_list)


if __name__ == "__main__":
    initPosCollection(dataReadyCallback, x)