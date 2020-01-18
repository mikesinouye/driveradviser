from subNats import *
from queue import Queue

"""
store single vehicle's data
data with a timestamp
"""
class IndividualPosition:
    def __init__(self, posData, timeStamp):
        self.posData = posData
        self.timeStamp = timeStamp

"""
predicts possible path region based off
of past data.
"""
class PathPredictor:
    def __init__(self):
        self.hasPosData = false
        self._MAX_QUEUE_SIZE = 200
        self.positions = Queue(self._MAX_QUEUE_SIZE)
        self.predictions = Queue(self._MAX_QUEUE_SIZE)

    def addData(self, positionData, timeStamp):
        """
        add new data to use
        """
        newPos = positionData(positionData, timeStamp)
        try:
            self.positions.put(newPos)
        except queue.Full:
            print("ERROR: QUEUE IS FULL")

    def predictPath(self):
        """
        - Predict path based off past path change.
        - Treat each datapoint as vector. compute change in angle,
        change in velocity between each point and its predecessor.
        predict next 8 seconds of data.
        - Find min/max for up to 8 seconds in past to create cone of
        possible future trajectory [could weight/average instead?]
        - Give confidence based off of accuracy of past prediction
        to actual [or make cone based off of this instead?]
        - inherit previous uncertainty and make it cone out for each point
        - returns list of predicted points and their error bands
        """
        