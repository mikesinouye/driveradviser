import numpy as np

# very small number so we dont divide by 0
EPSILON = 10**-3
INTERSECTION_TIME_MARGIN = 0.25



class Car:
    """
    init Car model
    """
    def __init__(self, x_position, y_position, x_velocity, y_velocity):
        self.x_position = x_position
        self.y_position = y_position
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity


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

        return ((self.x_position, self.x_velocity), (self.y_position, self.y_velocity))



    def update_info(self, x_position, y_position, x_velocity, y_velocity):
        self.x_position = x_position
        self.y_position = y_position
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity



    @staticmethod
    def predict_collision(car1, car2):

        # get the parametric equations for car1 and car2
        car1_x_eq, car1_y_eq = car1.calculate_parametric_equations()
        car2_x_eq, car2_y_eq = car2.calculate_parametric_equations()

        # check if the cars have the same x position and same x velocity
        if (car1_x_eq[0] == car2_x_eq[0]) and (car1_x_eq[1] == car2_x_eq[1]):
            # using np.inf to represent that there are infinite x_intersection times
            x_intersection_time = np.inf
        else:
            x_intersection_time = (car2_x_eq[0]-car1_x_eq[0]) / (car1_x_eq[1]-car2_x_eq[1] + EPSILON)

        # check if the cars have the same y position and same y velocity
        if (car1_y_eq[0] == car2_y_eq[0]) and (car1_y_eq[1] == car2_y_eq[1]):
            # using np.inf to represent that there are infinite y_intersection times
            y_intersection_time = np.inf
        else:
            y_intersection_time = (car2_y_eq[0]-car1_y_eq[0]) / (car1_y_eq[1]-car2_y_eq[1] + EPSILON)


        print("x_intersection_time: {}".format(x_intersection_time))
        print("y_intersection_time: {}".format(y_intersection_time))


        # check if the x intersection time is not all the time
        if not np.isinf(x_intersection_time):
            # calculate the intersection position
            x_intersection_pos = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time
        else:
            x_intersection_pos = car1_x_eq[0]


        # check if the y intersection time is not all the time
        if not np.isinf(y_intersection_time):
            # calculate the intersection position
            y_intersection_pos = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time
        else:
            y_intersection_pos = car1_y_eq[0]


        print("x_intersection_pos: {}".format(x_intersection_pos))
        print("y_intersection_pos: {}".format(y_intersection_pos))


        # check if both intersection times are non-negative
        if (x_intersection_time >= 0) and (y_intersection_time >= 0):

            if np.abs(x_intersection_time - y_intersection_time) < INTERSECTION_TIME_MARGIN or np.isinf(x_intersection_time) or np.isinf(y_intersection_time):
                print("WARNING, collision will occur at time: {}".format(x_intersection_time))
            elif np.abs(x_intersection_time - y_intersection_time) < INTERSECTION_TIME_MARGIN*8:
                print("WARNING, near miss will occur at time: {}".format(x_intersection_time))
            else:
                print("ALL CLEAR")

        else:
            print("ALL CLEAR")


