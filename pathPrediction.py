from subNats import *
from geopy import distance
import sys
sys.path.append('python/car_modeling')
from python.car_modeling.Car import *
import math
#from python.car_modeling.Car import *
"""
store single vehicle's data
data with a timestamp
"""
class IndividualPosition:
    def __init__(self, posData, timeStamp):
        self.posData = posData
        self.timeStamp = timeStamp
        #for parametric equation approach
        self.car = Car(posData.Latitude, posData.Longitude, posData.Heading, posData.Velocity)

"""
predicts possible path region based off
of past data.
"""
class PathPredictor:
    def __init__(self):
        self.hasPosData = False
        self._MAX_QUEUE_SIZE = 200
        self.positions = list()
        self.predictions = list()
        self.latestTime = 0
        self.timeRecordLength = 8
        self.latestCar = Car(0,0,0,0) #TODO: make this None and handle elsewhere

    def predictParams(self):
        # just return avg velocity, acceleration for now
        if len(self.positions) == 0:
            print("ERROR: queue shouldn't be empty")
            return (0, 0)
        elif len(self.positions) == 1:
            return (0, 0)
        else:
            # remove old datapoints
            self.positions = [pos for pos in self.positions if self.latestTime - pos.timeStamp < 8]
            print()

            # xVelocitySum = 0
            # yVelocitySum = 0
            xAccelerationSum = 0
            yAccelerationSum = 0
            size = len(self.positions)
            for i in range(size):
                # xVelocitySum += self.positions[i].Car.x_velocity
                # yVelocitySum += self.positions[i].Car.y_velocity
                if i != 0:
                    xAccelerationSum += self.positions[i].car.x_velocity - self.positions[i - 1].car.x_velocity
                    yAccelerationSum += self.positions[i].car.y_velocity - self.positions[i - 1].car.y_velocity

            return ((xAccelerationSum / (size - 1)), (yAccelerationSum / (size - 1)))

    def addData(self, positionData, timeStamp):
        """
        add new data to use
        """
        newPos = IndividualPosition(positionData, timeStamp)
        self.positions.append(newPos)
        self.predictedXAcceleration, self.predictedYAcceleration = self.predictParams()
        newPos.car.update_predictions(self.predictedXAcceleration, self.predictedYAcceleration)
        self.latestCar = newPos.car
        self.latestTime = timeStamp

    def predictPath(self, maxTime, resolution):
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
        #not anymore#- returns list of predicted points and their error bands
        - returns predicted acceleration, velocity
        - clears old timestamps if found
        """
        origin = (32.08595, -109.512)
        miles_per_km = 0.621371
        earth_radius = 3960.0
        degrees_to_radians = math.pi / 180.0
        radians_to_degrees = 180.0 / math.pi

        def change_in_latitude(miles):
            "Given a distance north, return the change in latitude."
            return (miles / earth_radius) * radians_to_degrees

        def change_in_longitude(latitude, miles):
            "Given a latitude and a distance west, return the change in longitude."
            # Find the radius of a circle around the earth at given latitude.
            r = earth_radius * math.cos(latitude * degrees_to_radians)
            return (miles / r) * radians_to_degrees

        """
        origin = (32.08595, -109.512)
        if latitude < 32.08595:
            self.y_position = -(distance.distance(origin, (latitude, -109.512)).km)
        else:
            self.y_position = (distance.distance(origin, (latitude, -109.512)).km)
        if longitude < -109.512:
            self.x_position = -(distance.distance(origin, (32.08595, longitude)).km)
        else:
            self.x_position = distance.distance(origin, (32.08595, longitude)).km
        """
        pointList = list()
        for t in np.linspace(0, maxTime, resolution):
            #find x,y at time based off of parametric equation
            x_eq, y_eq = self.latestCar.calculate_parametric_equations()
            x = x_eq[0] + x_eq[1]*t + 0.5*x_eq[2]*t*t
            y = y_eq[0] + y_eq[1]*t + 0.5*y_eq[2]*t*t
            #convert back to lat/lon
            d_lat = change_in_latitude(y*miles_per_km)
            lat = d_lat + origin[0]
            d_lon = change_in_longitude(lat, x*miles_per_km)
            lon = d_lon + origin[1]

            pointList.append([lat, lon])

        return pointList
