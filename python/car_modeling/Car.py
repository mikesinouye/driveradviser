import numpy as np
import math
from geopy import distance
# very small number so we dont divide by 0
EPSILON = 10**-6
INTERSECTION_TIME_MARGIN = 2/3600
NEAR_MISS_MULTIPLIER = 8


class Car:
    """
    init Car model
    """
    def __init__(self, x_position, y_position, x_velocity, y_velocity):
        self.x_position = x_position
        self.y_position = y_position
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.predicted_x_acceleration = 0
        self.predicted_y_acceleration = 0

    def __init__(self, latitude, longitude, heading, velocity):
        # 0 longitude is -109.512
        # 0 latitude is 32.08595
        origin = (32.08595, -109.512)
        if latitude < 32.08595:
            self.y_position = -(distance.distance(origin, (latitude, -109.512)).km)
        else:
            self.y_position = (distance.distance(origin, (latitude, -109.512)).km)
        if longitude < -109.512:
            self.x_position = -(distance.distance(origin, (32.08595, longitude)).km)
        else:
            self.x_position = distance.distance(origin, (32.08595, longitude)).km
        self.y_velocity = velocity * np.cos((np.pi * (heading-1)) / 180)
        self.x_velocity = velocity * np.sin((np.pi * (heading-1))/180)
        self.predicted_x_acceleration = 0
        self.predicted_y_acceleration = 0

    """
    input heading (as degrees clockwise from north) and speed
    return x_velocity (east direction as positive) and y_velocity (north direction as positive)
    """
    @staticmethod
    def heading_conversion(heading, speed):
        x_velocity = speed * np.sin((np.pi * heading)/180)
        y_velocity = speed * np.cos((np.pi * heading) / 180)
        return (x_velocity, y_velocity)


    """
    looks at the current state of the car, and returns parametric equations
    that model the cars predicted path
    """
    def calculate_parametric_equations(self):
        # return ((self.x_position, self.x_velocity, self.predicted_x_acceleration), (self.y_position, self.y_velocity, self.predicted_y_acceleration))
        return ((self.x_position, self.x_velocity,0), (self.y_position, self.y_velocity, 0))



    def update_info(self, x_position, y_position, x_velocity, y_velocity):
        self.x_position = x_position
        self.y_position = y_position
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
    
    def update_predictions(self, predicted_x_acceleration, predicted_y_acceleration):
        self.predicted_x_acceleration = predicted_x_acceleration
        self.predicted_y_acceleration = predicted_y_acceleration


    # @staticmethod
    # def predict_collision(car1, car2):
    #
    #     # get the parametric equations for car1 and car2
    #     car1_x_eq, car1_y_eq = car1.calculate_parametric_equations()
    #     car2_x_eq, car2_y_eq = car2.calculate_parametric_equations()
    #
    #     # check if the cars have the same x position and same x velocity and acceleration
    #     if (False and car1_x_eq[0] == car2_x_eq[0]) and (car1_x_eq[1] == car2_x_eq[1]) and (car1_x_eq[2] == car2_x_eq[2]):
    #         # using np.inf to represent that there are infinite x_intersection times
    #         x_intersection_time_1 = np.inf
    #         x_intersection_time_2 = np.inf
    #     else:
    #         a = car1_x_eq[2]
    #         b = car1_x_eq[1]
    #         c = car1_x_eq[0]
    #         d = car2_x_eq[2]
    #         e = car2_x_eq[1]
    #         f = car2_x_eq[0]
    #         #x_intersection_time_1 = (car2_x_eq[0]-car1_x_eq[0]) / (car1_x_eq[1]-car2_x_eq[1] + EPSILON)
    #         x_intersection_time_1 = (-1*(b - e) + np.sqrt((b - e)**2 - 2*(a - d)*(c - f)))/((a - d) + EPSILON)
    #         x_intersection_time_2 = (-1*(b - e) - np.sqrt((b - e)**2 - 2*(a - d)*(c - f)))/((a - d) + EPSILON)
    #
    #     # check if the cars have the same y position and same y velocity and acceleration
    #     if (False and car1_y_eq[0] == car2_y_eq[0]) and (car1_y_eq[1] == car2_y_eq[1]) and (car1_y_eq[2] == car2_y_eq[2]):
    #         # using np.inf to represent that there are infinite y_intersection times
    #         y_intersection_time_1 = np.inf
    #         y_intersection_time_2 = np.inf
    #     else:
    #         a = car1_y_eq[2]
    #         b = car1_y_eq[1]
    #         c = car1_y_eq[0]
    #         d = car2_y_eq[2]
    #         e = car2_y_eq[1]
    #         f = car2_y_eq[0]
    #         #y_intersection_time = (car2_y_eq[0]-car1_y_eq[0]) / (car1_y_eq[1]-car2_y_eq[1] + EPSILON)
    #         y_intersection_time_1 = (-1*(b - e) + np.sqrt((b - e)**2 - 2*(a - d)*(c - f)))/((a - d) + EPSILON)
    #         y_intersection_time_2 = (-1*(b - e) - np.sqrt((b - e)**2 - 2*(a - d)*(c - f)))/((a - d) + EPSILON)
    #
    #
    #     print("x_intersection_time_1: {}".format(x_intersection_time_1))
    #     print("y_intersection_time_1: {}".format(y_intersection_time_1))
    #     print("x_intersection_time_2: {}".format(x_intersection_time_2))
    #     print("y_intersection_time_2: {}".format(y_intersection_time_2))
    #
    #
    #     # check if the x intersection time is not all the time
    #     if not np.isinf(x_intersection_time_1):
    #         # calculate the intersection position
    #         x_intersection_pos_1 = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_1 + car1_x_eq[2] * x_intersection_time_1 ** 2
    #     else:
    #         x_intersection_pos_1 = car1_x_eq[0]
    #
    #     # check if the x intersection time is not all the time
    #     if not np.isinf(x_intersection_time_2):
    #         # calculate the intersection position
    #         x_intersection_pos_2 = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_2 + car1_x_eq[2] * x_intersection_time_2 ** 2
    #     else:
    #         x_intersection_pos_2 = car1_x_eq[0]
    #
    #     # check if the y intersection time is not all the time
    #     if not np.isinf(y_intersection_time_1):
    #         # calculate the intersection position
    #         y_intersection_pos_1 = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_1 + car1_y_eq[2] * y_intersection_time_1 ** 2
    #     else:
    #         y_intersection_pos_1 = car1_y_eq[0]
    #
    #     # check if the y intersection time is not all the time
    #     if not np.isinf(y_intersection_time_2):
    #         # calculate the intersection position
    #         y_intersection_pos_2 = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_2 + car1_y_eq[2] * y_intersection_time_2 ** 2
    #     else:
    #         y_intersection_pos_2 = car1_y_eq[0]
    #
    #
    #     print("x_intersection_pos_1: {}".format(x_intersection_pos_1))
    #     print("y_intersection_pos_1: {}".format(y_intersection_pos_1))
    #
    #     print("x_intersection_pos_2: {}".format(x_intersection_pos_1))
    #     print("y_intersection_pos_2: {}".format(y_intersection_pos_1))
    #
    #     #edge case: could be x and y times for different intercepts
    #     #TODO: handle if time
    #
    #     #TODO: detect near miss if within 3 seconds of impact when cleared. Need to store last calculated values
    #     #for impact time and
    #
    #     #TODO: send collision coordinate
    #
    #     # check if both intersection times are non-negative
    #     if (x_intersection_time_1 >= 0) and (y_intersection_time_1 >= 0) and not np.iscomplex(x_intersection_time_1) and not np.iscomplex(y_intersection_time_1):
    #         x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_1 + 0.5 * car1_x_eq[ 2] * x_intersection_time_1 ** 2
    #         y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_1 + 0.5 * car1_y_eq[2] * y_intersection_time_1 ** 2
    #         if np.abs(x_intersection_time_1 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN or np.isinf(x_intersection_time_1) or np.isinf(y_intersection_time_1):
    #             print("WARNING, collision will occur at time: {}".format(x_intersection_time_1))
    #             if(x_intersection_time_1 < 1):
    #                 return [4, x_intersection_time_1, [x_collision_position, y_collision_position]]
    #             elif x_intersection_time_1 < 5:
    #                 return [2, x_intersection_time_1, [x_collision_position, y_collision_position]]
    #             elif x_intersection_time_1 < 8:
    #                 return [1, x_intersection_time_1, [x_collision_position, y_collision_position]]
    #             else:
    #                 return [5, x_intersection_time_1]
    #         elif np.abs(x_intersection_time_1 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN*NEAR_MISS_MULTIPLIER:
    #             print("WARNING, near miss will occur at time: {}".format(x_intersection_time_1))
    #             if(x_intersection_time_1 < 1):
    #                 return [3, x_intersection_time_1, [x_collision_position, y_collision_position]]
    #         else:
    #             print("ALL CLEAR")
    #             return [5, x_intersection_time_1]
    #     elif (x_intersection_time_1 >= 0) and (y_intersection_time_2 >= 0) and not np.iscomplex(x_intersection_time_1) and not np.iscomplex(y_intersection_time_2):
    #         x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_1 + 0.5 * car1_x_eq[2] * x_intersection_time_1 ** 2
    #         y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_2 + 0.5 * car1_y_eq[2] * y_intersection_time_2 ** 2
    #         if np.abs(x_intersection_time_1 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN or np.isinf(x_intersection_time_1) or np.isinf(y_intersection_time_2):
    #             print("WARNING, collision will occur at time: {}".format(x_intersection_time_1))
    #             if(x_intersection_time_1 < 1):
    #                 return [4, x_intersection_time_1, [x_collision_position, y_collision_position]]
    #             elif x_intersection_time_1 < 5:
    #                 return [2, x_intersection_time_1, [x_collision_position, y_collision_position]]
    #             elif x_intersection_time_1 < 8:
    #                 return [1, x_intersection_time_1, [x_collision_position, y_collision_position]]
    #             else:
    #                 return [5, x_intersection_time_1]
    #         elif np.abs(x_intersection_time_1 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN*NEAR_MISS_MULTIPLIER:
    #             print("WARNING, near miss will occur at time: {}".format(x_intersection_time_1))
    #             if(x_intersection_time_1 < 1):
    #                 return [3, x_intersection_time_1, [x_collision_position, y_collision_position]]
    #         else:
    #             print("ALL CLEAR")
    #             return [5, x_intersection_time_1]
    #     elif (x_intersection_time_2 >= 0) and (y_intersection_time_1 >= 0) and not np.iscomplex(x_intersection_time_2) and not np.iscomplex(y_intersection_time_1):
    #         x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_2 + 0.5 * car1_x_eq[2] * x_intersection_time_2 ** 2
    #         y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_1 + 0.5 * car1_y_eq[2] * y_intersection_time_1 ** 2
    #         if np.abs(x_intersection_time_2 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN or np.isinf(x_intersection_time_2) or np.isinf(y_intersection_time_1):
    #             print("WARNING, collision will occur at time: {}".format(x_intersection_time_2))
    #             if(x_intersection_time_2 < 1):
    #                 return [4, x_intersection_time_2, [x_collision_position, y_collision_position]]
    #             elif x_intersection_time_1 < 5:
    #                 return [2, x_intersection_time_2, [x_collision_position, y_collision_position]]
    #             elif x_intersection_time_1 < 8:
    #                 return [1, x_intersection_time_2, [x_collision_position, y_collision_position]]
    #             else:
    #                 return [5, x_intersection_time_2]
    #         elif np.abs(x_intersection_time_2 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN*NEAR_MISS_MULTIPLIER:
    #             print("WARNING, near miss will occur at time: {}".format(x_intersection_time_2))
    #             if(x_intersection_time_2 < 1):
    #                 return [3, x_intersection_time_2, [x_collision_position, y_collision_position]]
    #         else:
    #             print("ALL CLEAR")
    #             return [5, x_intersection_time_2]
    #     elif (x_intersection_time_2 >= 0) and (y_intersection_time_2 >= 0) and not np.iscomplex(x_intersection_time_2) and not np.iscomplex(y_intersection_time_2):
    #         x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_2 + 0.5 * car1_x_eq[2] * x_intersection_time_2 ** 2
    #         y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_2 + 0.5 * car1_y_eq[2] * y_intersection_time_2 ** 2
    #         if np.abs(x_intersection_time_2 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN or np.isinf(x_intersection_time_2) or np.isinf(y_intersection_time_2):
    #             print("WARNING, collision will occur at time: {}".format(x_intersection_time_2))
    #             if(x_intersection_time_2 < 1):
    #                 return [4, x_intersection_time_2, [x_collision_position, y_collision_position]]
    #             elif x_intersection_time_1 < 5:
    #                 return [2, x_intersection_time_2, [x_collision_position, y_collision_position]]
    #             elif x_intersection_time_1 < 8:
    #                 return [1, x_intersection_time_2, [x_collision_position, y_collision_position]]
    #             else:
    #                 return [5, x_intersection_time_2]
    #         elif np.abs(x_intersection_time_2 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN*NEAR_MISS_MULTIPLIER:
    #             print("WARNING, near miss will occur at time: {}".format(x_intersection_time_2))
    #             if(x_intersection_time_2 < 1):
    #                 return [3, x_intersection_time_2, [x_collision_position, y_collision_position]]
    #         else:
    #             print("ALL CLEAR")
    #             return [5, x_intersection_time_2]
    #     else:
    #         print("ALL CLEAR")
    #         return [5, x_intersection_time_2]

    @staticmethod
    def predict_collision_lin(car1, car2):

        # get the parametric equations for car1 and car2
        car1_x_eq, car1_y_eq = car1.calculate_parametric_equations()
        car2_x_eq, car2_y_eq = car2.calculate_parametric_equations()

        # # check if the cars have the same x position and same x velocity and acceleration
        # if (False and car1_x_eq[0] == car2_x_eq[0]) and (car1_x_eq[1] == car2_x_eq[1]) and (
        #         car1_x_eq[2] == car2_x_eq[2]):
        #     # using np.inf to represent that there are infinite x_intersection times
        #     x_intersection_time_1 = np.inf
        #     x_intersection_time_2 = np.inf
        # else:
        #     a = car1_x_eq[2]
        #     b = car1_x_eq[1]
        #     c = car1_x_eq[0]
        #     d = car2_x_eq[2]
        #     e = car2_x_eq[1]
        #     f = car2_x_eq[0]
        #     # x_intersection_time_1 = (car2_x_eq[0]-car1_x_eq[0]) / (car1_x_eq[1]-car2_x_eq[1] + EPSILON)
        #     x_intersection_time_1 = (-1 * (b - e) + np.sqrt((b - e) ** 2 - 2 * (a - d) * (c - f))) / ((a - d) + EPSILON)
        #     x_intersection_time_2 = (-1 * (b - e) - np.sqrt((b - e) ** 2 - 2 * (a - d) * (c - f))) / ((a - d) + EPSILON)
        #
        # # check if the cars have the same y position and same y velocity and acceleration
        # if (False and car1_y_eq[0] == car2_y_eq[0]) and (car1_y_eq[1] == car2_y_eq[1]) and (
        #         car1_y_eq[2] == car2_y_eq[2]):
        #     # using np.inf to represent that there are infinite y_intersection times
        #     y_intersection_time_1 = np.inf
        #     y_intersection_time_2 = np.inf
        # else:
        #     a = car1_y_eq[2]
        #     b = car1_y_eq[1]
        #     c = car1_y_eq[0]
        #     d = car2_y_eq[2]
        #     e = car2_y_eq[1]
        #     f = car2_y_eq[0]
        #     # y_intersection_time = (car2_y_eq[0]-car1_y_eq[0]) / (car1_y_eq[1]-car2_y_eq[1] + EPSILON)
        #     y_intersection_time_1 = (-1 * (b - e) + np.sqrt((b - e) ** 2 - 2 * (a - d) * (c - f))) / ((a - d) + EPSILON)
        #     y_intersection_time_2 = (-1 * (b - e) - np.sqrt((b - e) ** 2 - 2 * (a - d) * (c - f))) / ((a - d) + EPSILON)


        if (car1_x_eq[1] - car2_x_eq[1]) < EPSILON:
            x_intersection_time_1 = np.inf
        else:
            x_intersection_time_1 = (car2_x_eq[0] - car1_x_eq[0]) / (car1_x_eq[1] - car2_x_eq[1])

        if (car1_y_eq[1] - car2_y_eq[1]) < EPSILON:
            y_intersection_time_1 = np.inf
        else:
            y_intersection_time_1 = (car2_y_eq[0] - car1_y_eq[0]) / (car1_y_eq[1] - car2_y_eq[1])


        if np.isinf(x_intersection_time_1) and np.isinf(y_intersection_time_1):
            print("\t\tSAME STARTING LOCATION")

        if np.isinf(x_intersection_time_1):
            x_intersection_time_1 = y_intersection_time_1

        if np.isinf(y_intersection_time_1):
            y_intersection_time_1 = x_intersection_time_1

        x_intersection_pos_1 = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_1
        y_intersection_pos_1 = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_1



        print("x_intersection_time_1: {}".format(x_intersection_time_1))
        print("y_intersection_time_1: {}".format(y_intersection_time_1))
        # print("x_intersection_time_2: {}".format(x_intersection_time_2))
        # print("y_intersection_time_2: {}".format(y_intersection_time_2))

        # # check if the x intersection time is not all the time
        # if not np.isinf(x_intersection_time_1):
        #     # calculate the intersection position
        #     x_intersection_pos_1 = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_1 + car1_x_eq[
        #         2] * x_intersection_time_1 ** 2
        # else:
        #     x_intersection_pos_1 = car1_x_eq[0]
        #
        # # check if the x intersection time is not all the time
        # if not np.isinf(x_intersection_time_2):
        #     # calculate the intersection position
        #     x_intersection_pos_2 = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_2 + car1_x_eq[
        #         2] * x_intersection_time_2 ** 2
        # else:
        #     x_intersection_pos_2 = car1_x_eq[0]
        #
        # # check if the y intersection time is not all the time
        # if not np.isinf(y_intersection_time_1):
        #     # calculate the intersection position
        #     y_intersection_pos_1 = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_1 + car1_y_eq[
        #         2] * y_intersection_time_1 ** 2
        # else:
        #     y_intersection_pos_1 = car1_y_eq[0]
        #
        # # check if the y intersection time is not all the time
        # if not np.isinf(y_intersection_time_2):
        #     # calculate the intersection position
        #     y_intersection_pos_2 = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_2 + car1_y_eq[
        #         2] * y_intersection_time_2 ** 2
        # else:
        #     y_intersection_pos_2 = car1_y_eq[0]

        print("x_intersection_pos_1: {}".format(x_intersection_pos_1))
        print("y_intersection_pos_1: {}".format(y_intersection_pos_1))

        # print("x_intersection_pos_2: {}".format(x_intersection_pos_1))
        # print("y_intersection_pos_2: {}".format(y_intersection_pos_1))

        # edge case: could be x and y times for different intercepts
        # TODO: handle if time

        # TODO: detect near miss if within 3 seconds of impact when cleared. Need to store last calculated values
        # for impact time and

        # TODO: send collision coordinate
        if (np.abs(x_intersection_time_1-y_intersection_time_1) < INTERSECTION_TIME_MARGIN and x_intersection_time_1>0 and y_intersection_time_1>0):
            print("\t\t WE GONNA DIEEE")

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


            # find x,y at time based off of parametric equation
            # x_eq, y_eq = self.latestCar.calculate_parametric_equations()
            # x = x_eq[0] + x_eq[1] * t + 0.5 * x_eq[2] * t * t
            x = x_intersection_pos_1

            # y = y_eq[0] + y_eq[1] * t + 0.5 * y_eq[2] * t * t
            y = y_intersection_pos_1

            # convert back to lat/lon
            d_lat = change_in_latitude(y * miles_per_km)
            lat = d_lat + origin[0]
            d_lon = change_in_longitude(lat, x * miles_per_km)
            lon = d_lon + origin[1]


















            print("coord: {}, {}".format(lat, lon))

            return [4, x_intersection_time_1, [lat, lon]]
        else:
            print("\t\t ALL CLEAR")
            return [5, x_intersection_time_1]

        #
        # # check if both intersection times are non-negative
        # if (x_intersection_time_1 >= 0) and (y_intersection_time_1 >= 0) and not np.iscomplex(
        #         x_intersection_time_1) and not np.iscomplex(y_intersection_time_1):
        #     x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_1 + 0.5 * car1_x_eq[
        #         2] * x_intersection_time_1 ** 2
        #     y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_1 + 0.5 * car1_y_eq[
        #         2] * y_intersection_time_1 ** 2
        #     if np.abs(x_intersection_time_1 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN or np.isinf(
        #             x_intersection_time_1) or np.isinf(y_intersection_time_1):
        #         print("WARNING, collision will occur at time: {}".format(x_intersection_time_1))
        #         if (x_intersection_time_1 < 1):
        #             return [4, x_intersection_time_1, [x_collision_position, y_collision_position]]
        #         elif x_intersection_time_1 < 5:
        #             return [2, x_intersection_time_1, [x_collision_position, y_collision_position]]
        #         elif x_intersection_time_1 < 8:
        #             return [1, x_intersection_time_1, [x_collision_position, y_collision_position]]
        #         else:
        #             return [5, x_intersection_time_1]
        #     elif np.abs(
        #             x_intersection_time_1 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN * NEAR_MISS_MULTIPLIER:
        #         print("WARNING, near miss will occur at time: {}".format(x_intersection_time_1))
        #         if (x_intersection_time_1 < 1):
        #             return [3, x_intersection_time_1, [x_collision_position, y_collision_position]]
        #     else:
        #         print("ALL CLEAR")
        #         return [5, x_intersection_time_1]
        # elif (x_intersection_time_1 >= 0) and (y_intersection_time_2 >= 0) and not np.iscomplex(
        #         x_intersection_time_1) and not np.iscomplex(y_intersection_time_2):
        #     x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_1 + 0.5 * car1_x_eq[
        #         2] * x_intersection_time_1 ** 2
        #     y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_2 + 0.5 * car1_y_eq[
        #         2] * y_intersection_time_2 ** 2
        #     if np.abs(x_intersection_time_1 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN or np.isinf(
        #             x_intersection_time_1) or np.isinf(y_intersection_time_2):
        #         print("WARNING, collision will occur at time: {}".format(x_intersection_time_1))
        #         if (x_intersection_time_1 < 1):
        #             return [4, x_intersection_time_1, [x_collision_position, y_collision_position]]
        #         elif x_intersection_time_1 < 5:
        #             return [2, x_intersection_time_1, [x_collision_position, y_collision_position]]
        #         elif x_intersection_time_1 < 8:
        #             return [1, x_intersection_time_1, [x_collision_position, y_collision_position]]
        #         else:
        #             return [5, x_intersection_time_1]
        #     elif np.abs(
        #             x_intersection_time_1 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN * NEAR_MISS_MULTIPLIER:
        #         print("WARNING, near miss will occur at time: {}".format(x_intersection_time_1))
        #         if (x_intersection_time_1 < 1):
        #             return [3, x_intersection_time_1, [x_collision_position, y_collision_position]]
        #     else:
        #         print("ALL CLEAR")
        #         return [5, x_intersection_time_1]
        # elif (x_intersection_time_2 >= 0) and (y_intersection_time_1 >= 0) and not np.iscomplex(
        #         x_intersection_time_2) and not np.iscomplex(y_intersection_time_1):
        #     x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_2 + 0.5 * car1_x_eq[
        #         2] * x_intersection_time_2 ** 2
        #     y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_1 + 0.5 * car1_y_eq[
        #         2] * y_intersection_time_1 ** 2
        #     if np.abs(x_intersection_time_2 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN or np.isinf(
        #             x_intersection_time_2) or np.isinf(y_intersection_time_1):
        #         print("WARNING, collision will occur at time: {}".format(x_intersection_time_2))
        #         if (x_intersection_time_2 < 1):
        #             return [4, x_intersection_time_2, [x_collision_position, y_collision_position]]
        #         elif x_intersection_time_1 < 5:
        #             return [2, x_intersection_time_2, [x_collision_position, y_collision_position]]
        #         elif x_intersection_time_1 < 8:
        #             return [1, x_intersection_time_2, [x_collision_position, y_collision_position]]
        #         else:
        #             return [5, x_intersection_time_2]
        #     elif np.abs(
        #             x_intersection_time_2 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN * NEAR_MISS_MULTIPLIER:
        #         print("WARNING, near miss will occur at time: {}".format(x_intersection_time_2))
        #         if (x_intersection_time_2 < 1):
        #             return [3, x_intersection_time_2, [x_collision_position, y_collision_position]]
        #     else:
        #         print("ALL CLEAR")
        #         return [5, x_intersection_time_2]
        # elif (x_intersection_time_2 >= 0) and (y_intersection_time_2 >= 0) and not np.iscomplex(
        #         x_intersection_time_2) and not np.iscomplex(y_intersection_time_2):
        #     x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_2 + 0.5 * car1_x_eq[
        #         2] * x_intersection_time_2 ** 2
        #     y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_2 + 0.5 * car1_y_eq[
        #         2] * y_intersection_time_2 ** 2
        #     if np.abs(x_intersection_time_2 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN or np.isinf(
        #             x_intersection_time_2) or np.isinf(y_intersection_time_2):
        #         print("WARNING, collision will occur at time: {}".format(x_intersection_time_2))
        #         if (x_intersection_time_2 < 1):
        #             return [4, x_intersection_time_2, [x_collision_position, y_collision_position]]
        #         elif x_intersection_time_1 < 5:
        #             return [2, x_intersection_time_2, [x_collision_position, y_collision_position]]
        #         elif x_intersection_time_1 < 8:
        #             return [1, x_intersection_time_2, [x_collision_position, y_collision_position]]
        #         else:
        #             return [5, x_intersection_time_2]
        #     elif np.abs(
        #             x_intersection_time_2 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN * NEAR_MISS_MULTIPLIER:
        #         print("WARNING, near miss will occur at time: {}".format(x_intersection_time_2))
        #         if (x_intersection_time_2 < 1):
        #             return [3, x_intersection_time_2, [x_collision_position, y_collision_position]]
        #     else:
        #         print("ALL CLEAR")
        #         return [5, x_intersection_time_2]
        # else:
        #     print("ALL CLEAR")
        #     return [5, x_intersection_time_2]


