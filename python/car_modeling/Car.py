import numpy as np
from geopy import distance
# very small number so we dont divide by 0
EPSILON = 10**-3
INTERSECTION_TIME_MARGIN = 0.25
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
        self.y_velocity = velocity * np.cos((np.pi * heading) / 180)
        self.x_velocity = velocity * np.sin((np.pi * heading)/180)
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
        # create simple parametric equations:

        # x = x_velocity * t + x_position
        # is represented as  (x_position, x_velocity)

        return ((self.x_position, self.x_velocity, self.predicted_x_acceleration), (self.y_position, self.y_velocity, self.predicted_y_acceleration))



    def update_info(self, x_position, y_position, x_velocity, y_velocity):
        self.x_position = x_position
        self.y_position = y_position
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
    
    def update_predictions(self, predicted_x_acceleration, predicted_y_acceleration):
        self.predicted_x_acceleration = predicted_x_acceleration
        self.predicted_y_acceleration = predicted_y_acceleration


    @staticmethod
    def predict_collision(car1, car2):

        # get the parametric equations for car1 and car2
        car1_x_eq, car1_y_eq = car1.calculate_parametric_equations()
        car2_x_eq, car2_y_eq = car2.calculate_parametric_equations()

        # check if the cars have the same x position and same x velocity and acceleration
        if (car1_x_eq[0] == car2_x_eq[0]) and (car1_x_eq[1] == car2_x_eq[1]) and (car1_x_eq[2] == car2_x_eq[2]):
            # using np.inf to represent that there are infinite x_intersection times
            x_intersection_time_1 = np.inf
            x_intersection_time_2 = np.inf
        else:
            a = car1_x_eq[0]
            b = car1_x_eq[1]
            c = car1_x_eq[2]
            d = car2_x_eq[0]
            e = car2_x_eq[1]
            f = car2_x_eq[2]
            #x_intersection_time_1 = (car2_x_eq[0]-car1_x_eq[0]) / (car1_x_eq[1]-car2_x_eq[1] + EPSILON)
            x_intersection_time_1 = (-1*(b - e) + np.sqrt((b - e)**2 - 4*(a - d)*(c - f)))/(2*(a - d) + EPSILON)
            x_intersection_time_2 = (-1*(b - e) - np.sqrt((b - e)**2 - 4*(a - d)*(c - f)))/(2*(a - d) + EPSILON)

        # check if the cars have the same y position and same y velocity and acceleration
        if (car1_y_eq[0] == car2_y_eq[0]) and (car1_y_eq[1] == car2_y_eq[1]) and (car1_y_eq[2] == car2_y_eq[2]):
            # using np.inf to represent that there are infinite y_intersection times
            y_intersection_time_1 = np.inf
            y_intersection_time_2 = np.inf
        else:
            a = car1_y_eq[0]
            b = car1_y_eq[1]
            c = car1_y_eq[2]
            d = car2_y_eq[0]
            e = car2_y_eq[1]
            f = car2_y_eq[2]
            #y_intersection_time = (car2_y_eq[0]-car1_y_eq[0]) / (car1_y_eq[1]-car2_y_eq[1] + EPSILON)
            y_intersection_time_1 = (-1*(b - e) + np.sqrt((b - e)**2 - 4*(a - d)*(c - f)))/(2*(a - d) + EPSILON)
            y_intersection_time_2 = (-1*(b - e) - np.sqrt((b - e)**2 - 4*(a - d)*(c - f)))/(2*(a - d) + EPSILON)

        print("x_intersection_time_1: {}".format(x_intersection_time_1))
        print("y_intersection_time_1: {}".format(y_intersection_time_1))
        print("x_intersection_time_2: {}".format(x_intersection_time_2))
        print("y_intersection_time_2: {}".format(y_intersection_time_2))


        # check if the x intersection time is not all the time
        if not np.isinf(x_intersection_time_1):
            # calculate the intersection position
            x_intersection_pos_1 = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_1 + car1_x_eq[2] * x_intersection_time_1 ** 2
        else:
            x_intersection_pos_1 = car1_x_eq[0]

        # check if the x intersection time is not all the time
        if not np.isinf(x_intersection_time_2):
            # calculate the intersection position
            x_intersection_pos_2 = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_2 + car1_x_eq[2] * x_intersection_time_2 ** 2
        else:
            x_intersection_pos_2 = car1_x_eq[0]

        # check if the y intersection time is not all the time
        if not np.isinf(y_intersection_time_1):
            # calculate the intersection position
            y_intersection_pos_1 = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_1 + car1_y_eq[2] * y_intersection_time_1 ** 2
        else:
            y_intersection_pos_1 = car1_y_eq[0]

        # check if the y intersection time is not all the time
        if not np.isinf(y_intersection_time_2):
            # calculate the intersection position
            y_intersection_pos_2 = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_2 + car1_y_eq[2] * y_intersection_time_2 ** 2
        else:
            y_intersection_pos_2 = car1_y_eq[0]


        print("x_intersection_pos_1: {}".format(x_intersection_pos_1))
        print("y_intersection_pos_1: {}".format(y_intersection_pos_1))
        
        print("x_intersection_pos_2: {}".format(x_intersection_pos_1))
        print("y_intersection_pos_2: {}".format(y_intersection_pos_1))

        # check if both intersection times are non-negative
        if (x_intersection_time_1 >= 0) and (y_intersection_time_1 >= 0) and np.iscomplex(x_intersection_time_1) and np.iscomplex(y_intersection_time_1):

            if np.abs(x_intersection_time_1 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN or np.isinf(x_intersection_time_1) or np.isinf(y_intersection_time_1):
                print("WARNING, collision will occur at time: {}".format(x_intersection_time_1))
            elif np.abs(x_intersection_time_1 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN*NEAR_MISS_MULTIPLIER:
                print("WARNING, near miss will occur at time: {}".format(x_intersection_time_1))
            else:
                print("ALL CLEAR")
        elif (x_intersection_time_1 >= 0) and (y_intersection_time_2 >= 0) and np.iscomplex(x_intersection_time_1) and np.iscomplex(y_intersection_time_2):

            if np.abs(x_intersection_time_1 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN or np.isinf(x_intersection_time_1) or np.isinf(y_intersection_time_2):
                print("WARNING, collision will occur at time: {}".format(x_intersection_time_1))
            elif np.abs(x_intersection_time_1 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN*NEAR_MISS_MULTIPLIER:
                print("WARNING, near miss will occur at time: {}".format(x_intersection_time_1))
            else:
                print("ALL CLEAR")
        elif (x_intersection_time_2 >= 0) and (y_intersection_time_1 >= 0) and np.iscomplex(x_intersection_time_2) and np.iscomplex(y_intersection_time_1):

            if np.abs(x_intersection_time_2 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN or np.isinf(x_intersection_time_2) or np.isinf(y_intersection_time_1):
                print("WARNING, collision will occur at time: {}".format(x_intersection_time_2))
            elif np.abs(x_intersection_time_2 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN*NEAR_MISS_MULTIPLIER:
                print("WARNING, near miss will occur at time: {}".format(x_intersection_time_2))
            else:
                print("ALL CLEAR")
        elif (x_intersection_time_2 >= 0) and (y_intersection_time_2 >= 0) and np.iscomplex(x_intersection_time_2) and np.iscomplex(y_intersection_time_2):

            if np.abs(x_intersection_time_2 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN or np.isinf(x_intersection_time_2) or np.isinf(y_intersection_time_2):
                print("WARNING, collision will occur at time: {}".format(x_intersection_time_2))
            elif np.abs(x_intersection_time_2 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN*NEAR_MISS_MULTIPLIER:
                print("WARNING, near miss will occur at time: {}".format(x_intersection_time_2))
            else:
                print("ALL CLEAR")
        else:
            print("ALL CLEAR")


