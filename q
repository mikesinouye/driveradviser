[1mdiff --git a/main.py b/main.py[m
[1mindex ec82d93..04248c9 100644[m
[1m--- a/main.py[m
[1m+++ b/main.py[m
[36m@@ -6,6 +6,7 @@[m [mimport sys[m
 x = -1[m
 if len(sys.argv) > 1:[m
     x = int(sys.argv[1])[m
[32m+[m[32m    x = 0[m
 else:[m
     x = 0[m
 [m
[36m@@ -39,16 +40,16 @@[m [mdef dataReadyCallback(dataPoint):[m
     else:[m
         target3Predictor.hasPosData = False[m
     #calc collisions and[m
[31m-    if(ownPredictor.hasPosData):[m
[32m+[m[32m    if(ownPredictor.hasPosData and ownPredictor.latestCar != None):[m
         return_list.append(ownPredictor.predictPath(8, 4))[m
[31m-        if(target1Predictor.hasPosData):[m
[31m-            alert_list.append(Car.predict_collision(ownPredictor.latestCar, target1Predictor.latestCar))[m
[32m+[m[32m        if(target1Predictor.hasPosData and target1Predictor.latestCar != None):[m
[32m+[m[32m            alert_list.append(Car.predict_collision_lin(ownPredictor.latestCar, target1Predictor.latestCar))[m
             return_list.append(target1Predictor.predictPath(8, 4))[m
[31m-        if(target2Predictor.hasPosData):[m
[31m-            alert_list.append(Car.predict_collision(ownPredictor.latestCar, target2Predictor.latestCar))[m
[32m+[m[32m        if(target2Predictor.hasPosData and target2Predictor.latestCar != None):[m
[32m+[m[32m            alert_list.append(Car.predict_collision_lin(ownPredictor.latestCar, target2Predictor.latestCar))[m
             return_list.append(target2Predictor.predictPath(8, 4))[m
[31m-        if(target3Predictor.hasPosData):[m
[31m-            alert_list.append(Car.predict_collision(ownPredictor.latestCar, target3Predictor.latestCar))[m
[32m+[m[32m        if(target3Predictor.hasPosData and target3Predictor.latestCar != None):[m
[32m+[m[32m            alert_list.append(Car.predict_collision_lin(ownPredictor.latestCar, target3Predictor.latestCar))[m
             return_list.append(target3Predictor.predictPath(8, 4))[m
 [m
     return (return_list, alert_list)[m
[1mdiff --git a/pathPrediction.py b/pathPrediction.py[m
[1mindex a91112f..988b505 100644[m
[1m--- a/pathPrediction.py[m
[1m+++ b/pathPrediction.py[m
[36m@@ -28,7 +28,7 @@[m [mclass PathPredictor:[m
         self.predictions = list()[m
         self.latestTime = 0[m
         self.timeRecordLength = 8[m
[31m-        self.latestCar = Car(0,0,0,0) #TODO: make this None and handle elsewhere[m
[32m+[m[32m        self.latestCar = None[m
 [m
     def predictParams(self):[m
         # just return avg velocity, acceleration for now[m
[36m@@ -68,6 +68,8 @@[m [mclass PathPredictor:[m
         self.latestTime = timeStamp[m
 [m
     def predictPath(self, maxTime, resolution):[m
[32m+[m[32m        if (self.latestCar == None):[m
[32m+[m[32m            return [] #return nothing if no cars yet[m
         """[m
         - Predict path based off past path change.[m
         - Treat each datapoint as vector. compute change in angle,[m
[1mdiff --git a/python/car_modeling/Car.py b/python/car_modeling/Car.py[m
[1mindex 484f6f0..6a68ec0 100644[m
[1m--- a/python/car_modeling/Car.py[m
[1m+++ b/python/car_modeling/Car.py[m
[36m@@ -2,7 +2,7 @@[m [mimport numpy as np[m
 from geopy import distance[m
 # very small number so we dont divide by 0[m
 EPSILON = 10**-6[m
[31m-INTERSECTION_TIME_MARGIN = 0.25[m
[32m+[m[32mINTERSECTION_TIME_MARGIN = 1[m
 NEAR_MISS_MULTIPLIER = 8[m
 [m
 [m
[36m@@ -30,8 +30,8 @@[m [mclass Car:[m
             self.x_position = -(distance.distance(origin, (32.08595, longitude)).km)[m
         else:[m
             self.x_position = distance.distance(origin, (32.08595, longitude)).km[m
[31m-        self.y_velocity = velocity * np.cos((np.pi * heading) / 180)[m
[31m-        self.x_velocity = velocity * np.sin((np.pi * heading)/180)[m
[32m+[m[32m        self.y_velocity = velocity * np.cos((np.pi * (heading-1)) / 180)[m
[32m+[m[32m        self.x_velocity = velocity * np.sin((np.pi * (heading-1))/180)[m
         self.predicted_x_acceleration = 0[m
         self.predicted_y_acceleration = 0[m
 [m
[36m@@ -51,12 +51,8 @@[m [mclass Car:[m
     that model the cars predicted path[m
     """[m
     def calculate_parametric_equations(self):[m
[31m-        # create simple parametric equations:[m
[31m-[m
[31m-        # x = x_velocity * t + x_position[m
[31m-        # is represented as  (x_position, x_velocity)[m
[31m-[m
[31m-        return ((self.x_position, self.x_velocity, self.predicted_x_acceleration), (self.y_position, self.y_velocity, self.predicted_y_acceleration))[m
[32m+[m[32m        # return ((self.x_position, self.x_velocity, self.predicted_x_acceleration), (self.y_position, self.y_velocity, self.predicted_y_acceleration))[m
[32m+[m[32m        return ((self.x_position, self.x_velocity,0), (self.y_position, self.y_velocity, 0))[m
 [m
 [m
 [m
[36m@@ -71,178 +67,408 @@[m [mclass Car:[m
         self.predicted_y_acceleration = predicted_y_acceleration[m
 [m
 [m
[32m+[m[32m    # @staticmethod[m
[32m+[m[32m    # def predict_collision(car1, car2):[m
[32m+[m[32m    #[m
[32m+[m[32m    #     # get the parametric equations for car1 and car2[m
[32m+[m[32m    #     car1_x_eq, car1_y_eq = car1.calculate_parametric_equations()[m
[32m+[m[32m    #     car2_x_eq, car2_y_eq = car2.calculate_parametric_equations()[m
[32m+[m[32m    #[m
[32m+[m[32m    #     # check if the cars have the same x position and same x velocity and acceleration[m
[32m+[m[32m    #     if (False and car1_x_eq[0] == car2_x_eq[0]) and (car1_x_eq[1] == car2_x_eq[1]) and (car1_x_eq[2] == car2_x_eq[2]):[m
[32m+[m[32m    #         # using np.inf to represent that there are infinite x_intersection times[m
[32m+[m[32m    #         x_intersection_time_1 = np.inf[m
[32m+[m[32m    #         x_intersection_time_2 = np.inf[m
[32m+[m[32m    #     else:[m
[32m+[m[32m    #         a = car1_x_eq[2][m
[32m+[m[32m    #         b = car1_x_eq[1][m
[32m+[m[32m    #         c = car1_x_eq[0][m
[32m+[m[32m    #         d = car2_x_eq[2][m
[32m+[m[32m    #         e = car2_x_eq[1][m
[32m+[m[32m    #         f = car2_x_eq[0][m
[32m+[m[32m    #         #x_intersection_time_1 = (car2_x_eq[0]-car1_x_eq[0]) / (car1_x_eq[1]-car2_x_eq[1] + EPSILON)[m
[32m+[m[32m    #         x_intersection_time_1 = (-1*(b - e) + np.sqrt((b - e)**2 - 2*(a - d)*(c - f)))/((a - d) + EPSILON)[m
[32m+[m[32m    #         x_intersection_time_2 = (-1*(b - e) - np.sqrt((b - e)**2 - 2*(a - d)*(c - f)))/((a - d) + EPSILON)[m
[32m+[m[32m    #[m
[32m+[m[32m    #     # check if the cars have the same y position and same y velocity and acceleration[m
[32m+[m[32m    #     if (False and car1_y_eq[0] == car2_y_eq[0]) and (car1_y_eq[1] == car2_y_eq[1]) and (car1_y_eq[2] == car2_y_eq[2]):[m
[32m+[m[32m    #         # using np.inf to represent that there are infinite y_intersection times[m
[32m+[m[32m    #         y_intersection_time_1 = np.inf[m
[32m+[m[32m    #         y_intersection_time_2 = np.inf[m
[32m+[m[32m    #     else:[m
[32m+[m[32m    #         a = car1_y_eq[2][m
[32m+[m[32m    #         b = car1_y_eq[1][m
[32m+[m[32m    #         c = car1_y_eq[0][m
[32m+[m[32m    #         d = car2_y_eq[2][m
[32m+[m[32m    #         e = car2_y_eq[1][m
[32m+[m[32m    #         f = car2_y_eq[0][m
[32m+[m[32m    #         #y_intersection_time = (car2_y_eq[0]-car1_y_eq[0]) / (car1_y_eq[1]-car2_y_eq[1] + EPSILON)[m
[32m+[m[32m    #         y_intersection_time_1 = (-1*(b - e) + np.sqrt((b - e)**2 - 2*(a - d)*(c - f)))/((a - d) + EPSILON)[m
[32m+[m[32m    #         y_intersection_time_2 = (-1*(b - e) - np.sqrt((b - e)**2 - 2*(a - d)*(c - f)))/((a - d) + EPSILON)[m
[32m+[m[32m    #[m
[32m+[m[32m    #[m
[32m+[m[32m    #     print("x_intersection_time_1: {}".format(x_intersection_time_1))[m
[32m+[m[32m    #     print("y_intersection_time_1: {}".format(y_intersection_time_1))[m
[32m+[m[32m    #     print("x_intersection_time_2: {}".format(x_intersection_time_2))[m
[32m+[m[32m    #     print("y_intersection_time_2: {}".format(y_intersection_time_2))[m
[32m+[m[32m    #[m
[32m+[m[32m    #[m
[32m+[m[32m    #     # check if the x intersection time is not all the time[m
[32m+[m[32m    #     if not np.isinf(x_intersection_time_1):[m
[32m+[m[32m    #         # calculate the intersection position[m
[32m+[m[32m    #         x_intersection_pos_1 = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_1 + car1_x_eq[2] * x_intersection_time_1 ** 2[m
[32m+[m[32m    #     else:[m
[32m+[m[32m    #         x_intersection_pos_1 = car1_x_eq[0][m
[32m+[m[32m    #[m
[32m+[m[32m    #     # check if the x intersection time is not all the time[m
[32m+[m[32m    #     if not np.isinf(x_intersection_time_2):[m
[32m+[m[32m    #         # calculate the intersection position[m
[32m+[m[32m    #         x_intersection_pos_2 = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_2 + car1_x_eq[2] * x_intersection_time_2 ** 2[m
[32m+[m[32m    #     else:[m
[32m+[m[32m    #         x_intersection_pos_2 = car1_x_eq[0][m
[32m+[m[32m    #[m
[32m+[m[32m    #     # check if the y intersection time is not all the time[m
[32m+[m[32m    #     if not np.isinf(y_intersection_time_1):[m
[32m+[m[32m    #         # calculate the intersection position[m
[32m+[m[32m    #         y_intersection_pos_1 = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_1 + car1_y_eq[2] * y_intersection_time_1 ** 2[m
[32m+[m[32m    #     else:[m
[32m+[m[32m    #         y_intersection_pos_1 = car1_y_eq[0][m
[32m+[m[32m    #[m
[32m+[m[32m    #     # check if the y intersection time is not all the time[m
[32m+[m[32m    #     if not np.isinf(y_intersection_time_2):[m
[32m+[m[32m    #         # calculate the intersection position[m
[32m+[m[32m    #         y_intersection_pos_2 = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_2 + car1_y_eq[2] * y_intersection_time_2 ** 2[m
[32m+[m[32m    #     else:[m
[32m+[m[32m    #         y_intersection_pos_2 = car1_y_eq[0][m
[32m+[m[32m    #[m
[32m+[m[32m    #[m
[32m+[m[32m    #     print("x_intersection_pos_1: {}".format(x_intersection_pos_1))[m
[32m+[m[32m    #     print("y_intersection_pos_1: {}".format(y_intersection_pos_1))[m
[32m+[m[32m    #[m
[32m+[m[32m    #     print("x_intersection_pos_2: {}".format(x_intersection_pos_1))[m
[32m+[m[32m    #     print("y_intersection_pos_2: {}".format(y_intersection_pos_1))[m
[32m+[m[32m    #[m
[32m+[m[32m    #     #edge case: could be x and y times for different intercepts[m
[32m+[m[32m    #     #TODO: handle if time[m
[32m+[m[32m    #[m
[32m+[m[32m    #     #TODO: detect near miss if within 3 seconds of impact when cleared. Need to store last calculated values[m
[32m+[m[32m    #     #for impact time and[m
[32m+[m[32m    #[m
[32m+[m[32m    #     #TODO: send collision coordinate[m
[32m+[m[32m    #[m
[32m+[m[32m    #     # check if both intersection times are non-negative[m
[32m+[m[32m    #     if (x_intersection_time_1 >= 0) and (y_intersection_time_1 >= 0) and not np.iscomplex(x_intersection_time_1) and not np.iscomplex(y_intersection_time_1):[m
[32m+[m[32m    #         x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_1 + 0.5 * car1_x_eq[ 2] * x_intersection_time_1 ** 2[m
[32m+[m[32m    #         y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_1 + 0.5 * car1_y_eq[2] * y_intersection_time_1 ** 2[m
[32m+[m[32m    #         if np.abs(x_intersection_time_1 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN or np.isinf(x_intersection_time_1) or np.isinf(y_intersection_time_1):[m
[32m+[m[32m    #             print("WARNING, collision will occur at time: {}".format(x_intersection_time_1))[m
[32m+[m[32m    #             if(x_intersection_time_1 < 1):[m
[32m+[m[32m    #                 return [4, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[32m+[m[32m    #             elif x_intersection_time_1 < 5:[m
[32m+[m[32m    #                 return [2, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[32m+[m[32m    #             elif x_intersection_time_1 < 8:[m
[32m+[m[32m    #                 return [1, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[32m+[m[32m    #             else:[m
[32m+[m[32m    #                 return [5, x_intersection_time_1][m
[32m+[m[32m    #         elif np.abs(x_intersection_time_1 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN*NEAR_MISS_MULTIPLIER:[m
[32m+[m[32m    #             print("WARNING, near miss will occur at time: {}".format(x_intersection_time_1))[m
[32m+[m[32m    #             if(x_intersection_time_1 < 1):[m
[32m+[m[32m    #                 return [3, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[32m+[m[32m    #         else:[m
[32m+[m[32m    #             print("ALL CLEAR")[m
[32m+[m[32m    #             return [5, x_intersection_time_1][m
[32m+[m[32m    #     elif (x_intersection_time_1 >= 0) and (y_intersection_time_2 >= 0) and not np.iscomplex(x_intersection_time_1) and not np.iscomplex(y_intersection_time_2):[m
[32m+[m[32m    #         x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_1 + 0.5 * car1_x_eq[2] * x_intersection_time_1 ** 2[m
[32m+[m[32m    #         y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_2 + 0.5 * car1_y_eq[2] * y_intersection_time_2 ** 2[m
[32m+[m[32m    #         if np.abs(x_intersection_time_1 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN or np.isinf(x_intersection_time_1) or np.isinf(y_intersection_time_2):[m
[32m+[m[32m    #             print("WARNING, collision will occur at time: {}".format(x_intersection_time_1))[m
[32m+[m[32m    #             if(x_intersection_time_1 < 1):[m
[32m+[m[32m    #                 return [4, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[32m+[m[32m    #             elif x_intersection_time_1 < 5:[m
[32m+[m[32m    #                 return [2, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[32m+[m[32m    #             elif x_intersection_time_1 < 8:[m
[32m+[m[32m    #                 return [1, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[32m+[m[32m    #             else:[m
[32m+[m[32m    #                 return [5, x_intersection_time_1][m
[32m+[m[32m    #         elif np.abs(x_intersection_time_1 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN*NEAR_MISS_MULTIPLIER:[m
[32m+[m[32m    #             print("WARNING, near miss will occur at time: {}".format(x_intersection_time_1))[m
[32m+[m[32m    #             if(x_intersection_time_1 < 1):[m
[32m+[m[32m    #                 return [3, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[32m+[m[32m    #         else:[m
[32m+[m[32m    #             print("ALL CLEAR")[m
[32m+[m[32m    #             return [5, x_intersection_time_1][m
[32m+[m[32m    #     elif (x_intersection_time_2 >= 0) and (y_intersection_time_1 >= 0) and not np.iscomplex(x_intersection_time_2) and not np.iscomplex(y_intersection_time_1):[m
[32m+[m[32m    #         x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_2 + 0.5 * car1_x_eq[2] * x_intersection_time_2 ** 2[m
[32m+[m[32m    #         y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_1 + 0.5 * car1_y_eq[2] * y_intersection_time_1 ** 2[m
[32m+[m[32m    #         if np.abs(x_intersection_time_2 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN or np.isinf(x_intersection_time_2) or np.isinf(y_intersection_time_1):[m
[32m+[m[32m    #             print("WARNING, collision will occur at time: {}".format(x_intersection_time_2))[m
[32m+[m[32m    #             if(x_intersection_time_2 < 1):[m
[32m+[m[32m    #                 return [4, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[32m+[m[32m    #             elif x_intersection_time_1 < 5:[m
[32m+[m[32m    #                 return [2, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[32m+[m[32m    #             elif x_intersection_time_1 < 8:[m
[32m+[m[32m    #                 return [1, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[32m+[m[32m    #             else:[m
[32m+[m[32m    #                 return [5, x_intersection_time_2][m
[32m+[m[32m    #         elif np.abs(x_intersection_time_2 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN*NEAR_MISS_MULTIPLIER:[m
[32m+[m[32m    #             print("WARNING, near miss will occur at time: {}".format(x_intersection_time_2))[m
[32m+[m[32m    #             if(x_intersection_time_2 < 1):[m
[32m+[m[32m    #                 return [3, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[32m+[m[32m    #         else:[m
[32m+[m[32m    #             print("ALL CLEAR")[m
[32m+[m[32m    #             return [5, x_intersection_time_2][m
[32m+[m[32m    #     elif (x_intersection_time_2 >= 0) and (y_intersection_time_2 >= 0) and not np.iscomplex(x_intersection_time_2) and not np.iscomplex(y_intersection_time_2):[m
[32m+[m[32m    #         x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_2 + 0.5 * car1_x_eq[2] * x_intersection_time_2 ** 2[m
[32m+[m[32m    #         y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_2 + 0.5 * car1_y_eq[2] * y_intersection_time_2 ** 2[m
[32m+[m[32m    #         if np.abs(x_intersection_time_2 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN or np.isinf(x_intersection_time_2) or np.isinf(y_intersection_time_2):[m
[32m+[m[32m    #             print("WARNING, collision will occur at time: {}".format(x_intersection_time_2))[m
[32m+[m[32m    #             if(x_intersection_time_2 < 1):[m
[32m+[m[32m    #                 return [4, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[32m+[m[32m    #             elif x_intersection_time_1 < 5:[m
[32m+[m[32m    #                 return [2, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[32m+[m[32m    #             elif x_intersection_time_1 < 8:[m
[32m+[m[32m    #                 return [1, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[32m+[m[32m    #             else:[m
[32m+[m[32m    #                 return [5, x_intersection_time_2][m
[32m+[m[32m    #         elif np.abs(x_intersection_time_2 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN*NEAR_MISS_MULTIPLIER:[m
[32m+[m[32m    #             print("WARNING, near miss will occur at time: {}".format(x_intersection_time_2))[m
[32m+[m[32m    #             if(x_intersection_time_2 < 1):[m
[32m+[m[32m    #                 return [3, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[32m+[m[32m    #         else:[m
[32m+[m[32m    #             print("ALL CLEAR")[m
[32m+[m[32m    #             return [5, x_intersection_time_2][m
[32m+[m[32m    #     else:[m
[32m+[m[32m    #         print("ALL CLEAR")[m
[32m+[m[32m    #         return [5, x_intersection_time_2][m
[32m+[m
     @staticmethod[m
[31m-    def predict_collision(car1, car2):[m
[32m+[m[32m    def predict_collision_lin(car1, car2):[m
 [m
         # get the parametric equations for car1 and car2[m
         car1_x_eq, car1_y_eq = car1.calculate_parametric_equations()[m
         car2_x_eq, car2_y_eq = car2.calculate_parametric_equations()[m
 [m
[31m-        # check if the cars have the same x position and same x velocity and acceleration[m
[31m-        if (False and car1_x_eq[0] == car2_x_eq[0]) and (car1_x_eq[1] == car2_x_eq[1]) and (car1_x_eq[2] == car2_x_eq[2]):[m
[31m-            # using np.inf to represent that there are infinite x_intersection times[m
[32m+[m[32m        # # check if the cars have the same x position and same x velocity and acceleration[m
[32m+[m[32m        # if (False and car1_x_eq[0] == car2_x_eq[0]) and (car1_x_eq[1] == car2_x_eq[1]) and ([m
[32m+[m[32m        #         car1_x_eq[2] == car2_x_eq[2]):[m
[32m+[m[32m        #     # using np.inf to represent that there are infinite x_intersection times[m
[32m+[m[32m        #     x_intersection_time_1 = np.inf[m
[32m+[m[32m        #     x_intersection_time_2 = np.inf[m
[32m+[m[32m        # else:[m
[32m+[m[32m        #     a = car1_x_eq[2][m
[32m+[m[32m        #     b = car1_x_eq[1][m
[32m+[m[32m        #     c = car1_x_eq[0][m
[32m+[m[32m        #     d = car2_x_eq[2][m
[32m+[m[32m        #     e = car2_x_eq[1][m
[32m+[m[32m        #     f = car2_x_eq[0][m
[32m+[m[32m        #     # x_intersection_time_1 = (car2_x_eq[0]-car1_x_eq[0]) / (car1_x_eq[1]-car2_x_eq[1] + EPSILON)[m
[32m+[m[32m        #     x_intersection_time_1 = (-1 * (b - e) + np.sqrt((b - e) ** 2 - 2 * (a - d) * (c - f))) / ((a - d) + EPSILON)[m
[32m+[m[32m        #     x_intersection_time_2 = (-1 * (b - e) - np.sqrt((b - e) ** 2 - 2 * (a - d) * (c - f))) / ((a - d) + EPSILON)[m
[32m+[m[32m        #[m
[32m+[m[32m        # # check if the cars have the same y position and same y velocity and acceleration[m
[32m+[m[32m        # if (False and car1_y_eq[0] == car2_y_eq[0]) and (car1_y_eq[1] == car2_y_eq[1]) and ([m
[32m+[m[32m        #         car1_y_eq[2] == car2_y_eq[2]):[m
[32m+[m[32m        #     # using np.inf to represent that there are infinite y_intersection times[m
[32m+[m[32m        #     y_intersection_time_1 = np.inf[m
[32m+[m[32m        #     y_intersection_time_2 = np.inf[m
[32m+[m[32m        # else:[m
[32m+[m[32m        #     a = car1_y_eq[2][m
[32m+[m[32m        #     b = car1_y_eq[1][m
[32m+[m[32m        #     c = car1_y_eq[0][m
[32m+[m[32m        #     d = car2_y_eq[2][m
[32m+[m[32m        #     e = car2_y_eq[1][m
[32m+[m[32m        #     f = car2_y_eq[0][m
[32m+[m[32m        #     # y_intersection_time = (car2_y_eq[0]-car1_y_eq[0]) / (car1_y_eq[1]-car2_y_eq[1] + EPSILON)[m
[32m+[m[32m        #     y_intersection_time_1 = (-1 * (b - e) + np.sqrt((b - e) ** 2 - 2 * (a - d) * (c - f))) / ((a - d) + EPSILON)[m
[32m+[m[32m        #     y_intersection_time_2 = (-1 * (b - e) - np.sqrt((b - e) ** 2 - 2 * (a - d) * (c - f))) / ((a - d) + EPSILON)[m
[32m+[m
[32m+[m
[32m+[m[32m        if (car1_x_eq[1] - car2_x_eq[1]) < EPSILON:[m
             x_intersection_time_1 = np.inf[m
[31m-            x_intersection_time_2 = np.inf[m
         else:[m
[31m-            a = car1_x_eq[2][m
[31m-            b = car1_x_eq[1][m
[31m-            c = car1_x_eq[0][m
[31m-            d = car2_x_eq[2][m
[31m-            e = car2_x_eq[1][m
[31m-            f = car2_x_eq[0][m
[31m-            #x_intersection_time_1 = (car2_x_eq[0]-car1_x_eq[0]) / (car1_x_eq[1]-car2_x_eq[1] + EPSILON)[m
[31m-            x_intersection_time_1 = (-1*(b - e) + np.sqrt((b - e)**2 - 2*(a - d)*(c - f)))/((a - d) + EPSILON)[m
[31m-            x_intersection_time_2 = (-1*(b - e) - np.sqrt((b - e)**2 - 2*(a - d)*(c - f)))/((a - d) + EPSILON)[m
[31m-[m
[31m-        # check if the cars have the same y position and same y velocity and acceleration[m
[31m-        if (False and car1_y_eq[0] == car2_y_eq[0]) and (car1_y_eq[1] == car2_y_eq[1]) and (car1_y_eq[2] == car2_y_eq[2]):[m
[31m-            # using np.inf to represent that there are infinite y_intersection times[m
[32m+[m[32m            x_intersection_time_1 = (car2_x_eq[0] - car1_x_eq[0]) / (car1_x_eq[1] - car2_x_eq[1])[m
[32m+[m
[32m+[m[32m        if (car1_y_eq[1] - car2_y_eq[1]) < EPSILON:[m
             y_intersection_time_1 = np.inf[m
[31m-            y_intersection_time_2 = np.inf[m
         else:[m
[31m-            a = car1_y_eq[2][m
[31m-            b = car1_y_eq[1][m
[31m-            c = car1_y_eq[0][m
[31m-            d = car2_y_eq[2][m
[31m-            e = car2_y_eq[1][m
[31m-            f = car2_y_eq[0][m
[31m-            #y_intersection_time = (car2_y_eq[0]-car1_y_eq[0]) / (car1_y_eq[1]-car2_y_eq[1] + EPSILON)[m
[31m-            y_intersection_time_1 = (-1*(b - e) + np.sqrt((b - e)**2 - 2*(a - d)*(c - f)))/((a - d) + EPSILON)[m
[31m-            y_intersection_time_2 = (-1*(b - e) - np.sqrt((b - e)**2 - 2*(a - d)*(c - f)))/((a - d) + EPSILON)[m
[32m+[m[32m            y_intersection_time_1 = (car2_y_eq[0] - car1_y_eq[0]) / (car1_y_eq[1] - car2_y_eq[1])[m
 [m
 [m
[31m-        print("x_intersection_time_1: {}".format(x_intersection_time_1))[m
[31m-        print("y_intersection_time_1: {}".format(y_intersection_time_1))[m
[31m-        print("x_intersection_time_2: {}".format(x_intersection_time_2))[m
[31m-        print("y_intersection_time_2: {}".format(y_intersection_time_2))[m
[32m+[m[32m        if np.isinf(x_intersection_time_1) and np.isinf(y_intersection_time_1):[m
[32m+[m[32m            print("\t\tSAME STARTING LOCATION")[m
 [m
[32m+[m[32m        if np.isinf(x_intersection_time_1):[m
[32m+[m[32m            x_intersection_time_1 = y_intersection_time_1[m
 [m
[31m-        # check if the x intersection time is not all the time[m
[31m-        if not np.isinf(x_intersection_time_1):[m
[31m-            # calculate the intersection position[m
[31m-            x_intersection_pos_1 = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_1 + car1_x_eq[2] * x_intersection_time_1 ** 2[m
[31m-        else:[m
[31m-            x_intersection_pos_1 = car1_x_eq[0][m
[32m+[m[32m        if np.isinf(y_intersection_time_1):[m
[32m+[m[32m            y_intersection_time_1 = x_intersection_time_1[m
 [m
[31m-        # check if the x intersection time is not all the time[m
[31m-        if not np.isinf(x_intersection_time_2):[m
[31m-            # calculate the intersection position[m
[31m-            x_intersection_pos_2 = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_2 + car1_x_eq[2] * x_intersection_time_2 ** 2[m
[31m-        else:[m
[31m-            x_intersection_pos_2 = car1_x_eq[0][m
[32m+[m[32m        x_intersection_pos_1 = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_1[m
[32m+[m[32m        y_intersection_pos_1 = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_1[m
 [m
[31m-        # check if the y intersection time is not all the time[m
[31m-        if not np.isinf(y_intersection_time_1):[m
[31m-            # calculate the intersection position[m
[31m-            y_intersection_pos_1 = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_1 + car1_y_eq[2] * y_intersection_time_1 ** 2[m
[31m-        else:[m
[31m-            y_intersection_pos_1 = car1_y_eq[0][m
 [m
[31m-        # check if the y intersection time is not all the time[m
[31m-        if not np.isinf(y_intersection_time_2):[m
[31m-            # calculate the intersection position[m
[31m-            y_intersection_pos_2 = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_2 + car1_y_eq[2] * y_intersection_time_2 ** 2[m
[31m-        else:[m
[31m-            y_intersection_pos_2 = car1_y_eq[0][m
 [m
[32m+[m[32m        print("x_intersection_time_1: {}".format(x_intersection_time_1))[m
[32m+[m[32m        print("y_intersection_time_1: {}".format(y_intersection_time_1))[m
[32m+[m[32m        # print("x_intersection_time_2: {}".format(x_intersection_time_2))[m
[32m+[m[32m        # print("y_intersection_time_2: {}".format(y_intersection_time_2))[m
[32m+[m
[32m+[m[32m        # # check if the x intersection time is not all the time[m
[32m+[m[32m        # if not np.isinf(x_intersection_time_1):[m
[32m+[m[32m        #     # calculate the intersection position[m
[32m+[m[32m        #     x_intersection_pos_1 = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_1 + car1_x_eq[[m
[32m+[m[32m        #         2] * x_intersection_time_1 ** 2[m
[32m+[m[32m        # else:[m
[32m+[m[32m        #     x_intersection_pos_1 = car1_x_eq[0][m
[32m+[m[32m        #[m
[32m+[m[32m        # # check if the x intersection time is not all the time[m
[32m+[m[32m        # if not np.isinf(x_intersection_time_2):[m
[32m+[m[32m        #     # calculate the intersection position[m
[32m+[m[32m        #     x_intersection_pos_2 = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_2 + car1_x_eq[[m
[32m+[m[32m        #         2] * x_intersection_time_2 ** 2[m
[32m+[m[32m        # else:[m
[32m+[m[32m        #     x_intersection_pos_2 = car1_x_eq[0][m
[32m+[m[32m        #[m
[32m+[m[32m        # # check if the y intersection time is not all the time[m
[32m+[m[32m        # if not np.isinf(y_intersection_time_1):[m
[32m+[m[32m        #     # calculate the intersection position[m
[32m+[m[32m        #     y_intersection_pos_1 = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_1 + car1_y_eq[[m
[32m+[m[32m        #         2] * y_intersection_time_1 ** 2[m
[32m+[m[32m        # else:[m
[32m+[m[32m        #     y_intersection_pos_1 = car1_y_eq[0][m
[32m+[m[32m        #[m
[32m+[m[32m        # # check if the y intersection time is not all the time[m
[32m+[m[32m        # if not np.isinf(y_intersection_time_2):[m
[32m+[m[32m        #     # calculate the intersection position[m
[32m+[m[32m        #     y_intersection_pos_2 = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_2 + car1_y_eq[[m
[32m+[m[32m        #         2] * y_intersection_time_2 ** 2[m
[32m+[m[32m        # else:[m
[32m+[m[32m        #     y_intersection_pos_2 = car1_y_eq[0][m
 [m
         print("x_intersection_pos_1: {}".format(x_intersection_pos_1))[m
         print("y_intersection_pos_1: {}".format(y_intersection_pos_1))[m
[31m-        [m
[31m-        print("x_intersection_pos_2: {}".format(x_intersection_pos_1))[m
[31m-        print("y_intersection_pos_2: {}".format(y_intersection_pos_1))[m
[31m-[m
[31m-        #edge case: could be x and y times for different intercepts[m
[31m-        #TODO: handle if time[m
[31m-[m
[31m-        #TODO: detect near miss if within 3 seconds of impact when cleared. Need to store last calculated values[m
[31m-        #for impact time and[m
[31m-[m
[31m-        #TODO: send collision coordinate[m
[31m-[m
[31m-        # check if both intersection times are non-negative[m
[31m-        if (x_intersection_time_1 >= 0) and (y_intersection_time_1 >= 0) and not np.iscomplex(x_intersection_time_1) and not np.iscomplex(y_intersection_time_1):[m
[31m-            x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_1 + 0.5 * car1_x_eq[ 2] * x_intersection_time_1 ** 2[m
[31m-            y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_1 + 0.5 * car1_y_eq[2] * y_intersection_time_1 ** 2[m
[31m-            if np.abs(x_intersection_time_1 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN or np.isinf(x_intersection_time_1) or np.isinf(y_intersection_time_1):[m
[31m-                print("WARNING, collision will occur at time: {}".format(x_intersection_time_1))[m
[31m-                if(x_intersection_time_1 < 1):[m
[31m-                    return [4, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[31m-                elif x_intersection_time_1 < 5:[m
[31m-                    return [2, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[31m-                elif x_intersection_time_1 < 8:[m
[31m-                    return [1, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[31m-                else:[m
[31m-                    return [5, x_intersection_time_1][m
[31m-            elif np.abs(x_intersection_time_1 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN*NEAR_MISS_MULTIPLIER:[m
[31m-                print("WARNING, near miss will occur at time: {}".format(x_intersection_time_1))[m
[31m-                if(x_intersection_time_1 < 1):[m
[31m-                    return [3, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[31m-            else:[m
[31m-                print("ALL CLEAR")[m
[31m-                return [5, x_intersection_time_1][m
[31m-        elif (x_intersection_time_1 >= 0) and (y_intersection_time_2 >= 0) and not np.iscomplex(x_intersection_time_1) and not np.iscomplex(y_intersection_time_2):[m
[31m-            x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_1 + 0.5 * car1_x_eq[2] * x_intersection_time_1 ** 2[m
[31m-            y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_2 + 0.5 * car1_y_eq[2] * y_intersection_time_2 ** 2[m
[31m-            if np.abs(x_intersection_time_1 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN or np.isinf(x_intersection_time_1) or np.isinf(y_intersection_time_2):[m
[31m-                print("WARNING, collision will occur at time: {}".format(x_intersection_time_1))[m
[31m-                if(x_intersection_time_1 < 1):[m
[31m-                    return [4, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[31m-                elif x_intersection_time_1 < 5:[m
[31m-                    return [2, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[31m-                elif x_intersection_time_1 < 8:[m
[31m-                    return [1, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[31m-                else:[m
[31m-                    return [5, x_intersection_time_1][m
[31m-            elif np.abs(x_intersection_time_1 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN*NEAR_MISS_MULTIPLIER:[m
[31m-                print("WARNING, near miss will occur at time: {}".format(x_intersection_time_1))[m
[31m-                if(x_intersection_time_1 < 1):[m
[31m-                    return [3, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[31m-            else:[m
[31m-                print("ALL CLEAR")[m
[31m-                return [5, x_intersection_time_1][m
[31m-        elif (x_intersection_time_2 >= 0) and (y_intersection_time_1 >= 0) and not np.iscomplex(x_intersection_time_2) and not np.iscomplex(y_intersection_time_1):[m
[31m-            x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_2 + 0.5 * car1_x_eq[2] * x_intersection_time_2 ** 2[m
[31m-            y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_1 + 0.5 * car1_y_eq[2] * y_intersection_time_1 ** 2[m
[31m-            if np.abs(x_intersection_time_2 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN or np.isinf(x_intersection_time_2) or np.isinf(y_intersection_time_1):[m
[31m-                print("WARNING, collision will occur at time: {}".format(x_intersection_time_2))[m
[31m-                if(x_intersection_time_2 < 1):[m
[31m-                    return [4, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[31m-                elif x_intersection_time_1 < 5:[m
[31m-                    return [2, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[31m-                elif x_intersection_time_1 < 8:[m
[31m-                    return [1, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[31m-                else:[m
[31m-                    return [5, x_intersection_time_2][m
[31m-            elif np.abs(x_intersection_time_2 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN*NEAR_MISS_MULTIPLIER:[m
[31m-                print("WARNING, near miss will occur at time: {}".format(x_intersection_time_2))[m
[31m-                if(x_intersection_time_2 < 1):[m
[31m-                    return [3, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[31m-            else:[m
[31m-                print("ALL CLEAR")[m
[31m-                return [5, x_intersection_time_2][m
[31m-        elif (x_intersection_time_2 >= 0) and (y_intersection_time_2 >= 0) and not np.iscomplex(x_intersection_time_2) and not np.iscomplex(y_intersection_time_2):[m
[31m-            x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_2 + 0.5 * car1_x_eq[2] * x_intersection_time_2 ** 2[m
[31m-            y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_2 + 0.5 * car1_y_eq[2] * y_intersection_time_2 ** 2[m
[31m-            if np.abs(x_intersection_time_2 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN or np.isinf(x_intersection_time_2) or np.isinf(y_intersection_time_2):[m
[31m-                print("WARNING, collision will occur at time: {}".format(x_intersection_time_2))[m
[31m-                if(x_intersection_time_2 < 1):[m
[31m-                    return [4, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[31m-                elif x_intersection_time_1 < 5:[m
[31m-                    return [2, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[31m-                elif x_intersection_time_1 < 8:[m
[31m-                    return [1, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[31m-                else:[m
[31m-                    return [5, x_intersection_time_2][m
[31m-            elif np.abs(x_intersection_time_2 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN*NEAR_MISS_MULTIPLIER:[m
[31m-                print("WARNING, near miss will occur at time: {}".format(x_intersection_time_2))[m
[31m-                if(x_intersection_time_2 < 1):[m
[31m-                    return [3, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[31m-            else:[m
[31m-                print("ALL CLEAR")[m
[31m-                return [5, x_intersection_time_2][m
[32m+[m
[32m+[m[32m        # print("x_intersection_pos_2: {}".format(x_intersection_pos_1))[m
[32m+[m[32m        # print("y_intersection_pos_2: {}".format(y_intersection_pos_1))[m
[32m+[m
[32m+[m[32m        # edge case: could be x and y times for different intercepts[m
[32m+[m[32m        # TODO: handle if time[m
[32m+[m
[32m+[m[32m        # TODO: detect near miss if within 3 seconds of impact when cleared. Need to store last calculated values[m
[32m+[m[32m        # for impact time and[m
[32m+[m
[32m+[m[32m        # TODO: send collision coordinate[m
[32m+[m[32m        if (np.abs(x_intersection_time_1-y_intersection_time_1) < INTERSECTION_TIME_MARGIN and x_intersection_time_1>0 and y_intersection_time_1>0):[m
[32m+[m[32m            print("\t\t WE GONNA DIEEE")[m
[32m+[m[32m            return [4, x_intersection_time_1, [x_intersection_pos_1, y_intersection_pos_1]][m
         else:[m
[31m-            print("ALL CLEAR")[m
[31m-            return [5, x_intersection_time_2][m
[32m+[m[32m            print("\t\t ALL CLEAR")[m
[32m+[m[32m            return [5, x_intersection_time_1][m
[32m+[m
[32m+[m[32m        #[m
[32m+[m[32m        # # check if both intersection times are non-negative[m
[32m+[m[32m        # if (x_intersection_time_1 >= 0) and (y_intersection_time_1 >= 0) and not np.iscomplex([m
[32m+[m[32m        #         x_intersection_time_1) and not np.iscomplex(y_intersection_time_1):[m
[32m+[m[32m        #     x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_1 + 0.5 * car1_x_eq[[m
[32m+[m[32m        #         2] * x_intersection_time_1 ** 2[m
[32m+[m[32m        #     y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_1 + 0.5 * car1_y_eq[[m
[32m+[m[32m        #         2] * y_intersection_time_1 ** 2[m
[32m+[m[32m        #     if np.abs(x_intersection_time_1 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN or np.isinf([m
[32m+[m[32m        #             x_intersection_time_1) or np.isinf(y_intersection_time_1):[m
[32m+[m[32m        #         print("WARNING, collision will occur at time: {}".format(x_intersection_time_1))[m
[32m+[m[32m        #         if (x_intersection_time_1 < 1):[m
[32m+[m[32m        #             return [4, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[32m+[m[32m        #         elif x_intersection_time_1 < 5:[m
[32m+[m[32m        #             return [2, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[32m+[m[32m        #         elif x_intersection_time_1 < 8:[m
[32m+[m[32m        #             return [1, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[32m+[m[32m        #         else:[m
[32m+[m[32m        #             return [5, x_intersection_time_1][m
[32m+[m[32m        #     elif np.abs([m
[32m+[m[32m        #             x_intersection_time_1 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN * NEAR_MISS_MULTIPLIER:[m
[32m+[m[32m        #         print("WARNING, near miss will occur at time: {}".format(x_intersection_time_1))[m
[32m+[m[32m        #         if (x_intersection_time_1 < 1):[m
[32m+[m[32m        #             return [3, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[32m+[m[32m        #     else:[m
[32m+[m[32m        #         print("ALL CLEAR")[m
[32m+[m[32m        #         return [5, x_intersection_time_1][m
[32m+[m[32m        # elif (x_intersection_time_1 >= 0) and (y_intersection_time_2 >= 0) and not np.iscomplex([m
[32m+[m[32m        #         x_intersection_time_1) and not np.iscomplex(y_intersection_time_2):[m
[32m+[m[32m        #     x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_1 + 0.5 * car1_x_eq[[m
[32m+[m[32m        #         2] * x_intersection_time_1 ** 2[m
[32m+[m[32m        #     y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_2 + 0.5 * car1_y_eq[[m
[32m+[m[32m        #         2] * y_intersection_time_2 ** 2[m
[32m+[m[32m        #     if np.abs(x_intersection_time_1 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN or np.isinf([m
[32m+[m[32m        #             x_intersection_time_1) or np.isinf(y_intersection_time_2):[m
[32m+[m[32m        #         print("WARNING, collision will occur at time: {}".format(x_intersection_time_1))[m
[32m+[m[32m        #         if (x_intersection_time_1 < 1):[m
[32m+[m[32m        #             return [4, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[32m+[m[32m        #         elif x_intersection_time_1 < 5:[m
[32m+[m[32m        #             return [2, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[32m+[m[32m        #         elif x_intersection_time_1 < 8:[m
[32m+[m[32m        #             return [1, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[32m+[m[32m        #         else:[m
[32m+[m[32m        #             return [5, x_intersection_time_1][m
[32m+[m[32m        #     elif np.abs([m
[32m+[m[32m        #             x_intersection_time_1 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN * NEAR_MISS_MULTIPLIER:[m
[32m+[m[32m        #         print("WARNING, near miss will occur at time: {}".format(x_intersection_time_1))[m
[32m+[m[32m        #         if (x_intersection_time_1 < 1):[m
[32m+[m[32m        #             return [3, x_intersection_time_1, [x_collision_position, y_collision_position]][m
[32m+[m[32m        #     else:[m
[32m+[m[32m        #         print("ALL CLEAR")[m
[32m+[m[32m        #         return [5, x_intersection_time_1][m
[32m+[m[32m        # elif (x_intersection_time_2 >= 0) and (y_intersection_time_1 >= 0) and not np.iscomplex([m
[32m+[m[32m        #         x_intersection_time_2) and not np.iscomplex(y_intersection_time_1):[m
[32m+[m[32m        #     x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_2 + 0.5 * car1_x_eq[[m
[32m+[m[32m        #         2] * x_intersection_time_2 ** 2[m
[32m+[m[32m        #     y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_1 + 0.5 * car1_y_eq[[m
[32m+[m[32m        #         2] * y_intersection_time_1 ** 2[m
[32m+[m[32m        #     if np.abs(x_intersection_time_2 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN or np.isinf([m
[32m+[m[32m        #             x_intersection_time_2) or np.isinf(y_intersection_time_1):[m
[32m+[m[32m        #         print("WARNING, collision will occur at time: {}".format(x_intersection_time_2))[m
[32m+[m[32m        #         if (x_intersection_time_2 < 1):[m
[32m+[m[32m        #             return [4, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[32m+[m[32m        #         elif x_intersection_time_1 < 5:[m
[32m+[m[32m        #             return [2, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[32m+[m[32m        #         elif x_intersection_time_1 < 8:[m
[32m+[m[32m        #             return [1, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[32m+[m[32m        #         else:[m
[32m+[m[32m        #             return [5, x_intersection_time_2][m
[32m+[m[32m        #     elif np.abs([m
[32m+[m[32m        #             x_intersection_time_2 - y_intersection_time_1) < INTERSECTION_TIME_MARGIN * NEAR_MISS_MULTIPLIER:[m
[32m+[m[32m        #         print("WARNING, near miss will occur at time: {}".format(x_intersection_time_2))[m
[32m+[m[32m        #         if (x_intersection_time_2 < 1):[m
[32m+[m[32m        #             return [3, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[32m+[m[32m        #     else:[m
[32m+[m[32m        #         print("ALL CLEAR")[m
[32m+[m[32m        #         return [5, x_intersection_time_2][m
[32m+[m[32m        # elif (x_intersection_time_2 >= 0) and (y_intersection_time_2 >= 0) and not np.iscomplex([m
[32m+[m[32m        #         x_intersection_time_2) and not np.iscomplex(y_intersection_time_2):[m
[32m+[m[32m        #     x_collision_position = car1_x_eq[0] + car1_x_eq[1] * x_intersection_time_2 + 0.5 * car1_x_eq[[m
[32m+[m[32m        #         2] * x_intersection_time_2 ** 2[m
[32m+[m[32m        #     y_collision_position = car1_y_eq[0] + car1_y_eq[1] * y_intersection_time_2 + 0.5 * car1_y_eq[[m
[32m+[m[32m        #         2] * y_intersection_time_2 ** 2[m
[32m+[m[32m        #     if np.abs(x_intersection_time_2 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN or np.isinf([m
[32m+[m[32m        #             x_intersection_time_2) or np.isinf(y_intersection_time_2):[m
[32m+[m[32m        #         print("WARNING, collision will occur at time: {}".format(x_intersection_time_2))[m
[32m+[m[32m        #         if (x_intersection_time_2 < 1):[m
[32m+[m[32m        #             return [4, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[32m+[m[32m        #         elif x_intersection_time_1 < 5:[m
[32m+[m[32m        #             return [2, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[32m+[m[32m        #         elif x_intersection_time_1 < 8:[m
[32m+[m[32m        #             return [1, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[32m+[m[32m        #         else:[m
[32m+[m[32m        #             return [5, x_intersection_time_2][m
[32m+[m[32m        #     elif np.abs([m
[32m+[m[32m        #             x_intersection_time_2 - y_intersection_time_2) < INTERSECTION_TIME_MARGIN * NEAR_MISS_MULTIPLIER:[m
[32m+[m[32m        #         print("WARNING, near miss will occur at time: {}".format(x_intersection_time_2))[m
[32m+[m[32m        #         if (x_intersection_time_2 < 1):[m
[32m+[m[32m        #             return [3, x_intersection_time_2, [x_collision_position, y_collision_position]][m
[32m+[m[32m        #     else:[m
[32m+[m[32m        #         print("ALL CLEAR")[m
[32m+[m[32m        #         return [5, x_intersection_time_2][m
[32m+[m[32m        # else:[m
[32m+[m[32m        #     print("ALL CLEAR")[m
[32m+[m[32m        #     return [5, x_intersection_time_2][m
 [m
 [m
[1mdiff --git a/subNats.py b/subNats.py[m
[1mindex 8a157dd..8b33731 100644[m
[1m--- a/subNats.py[m
[1m+++ b/subNats.py[m
[36m@@ -111,7 +111,7 @@[m [masync def run(loop, dataAddedCallback, curr_scenario):[m
         # outfile.write(DataPoints(positionModel, timestamp).to_json())[m
         # outfile.close()[m
         # car1 = Car(newdata.positionModel.OwnPosition.Latitude, newdata.positionModel.OwnPosition.Longitude,[m
[31m-        #            newdata.positionModel.OwnPosition.Heading, newdata.positionModel.OwnPosition.Velocity)[m
[32m+[m[32m        #        (    newdata.positionModel.OwnPosition.Heading, newdata.positionModel.OwnPosition.Velocity))[m
         # car2 = Car(newdata.positionModel.Target1Position.Latitude, newdata.positionModel.Target1Position.Longitude,[m
         #            newdata.positionModel.Target1Position.Heading, newdata.positionModel.Target1Position.Velocity)[m
         # car1.predict_collision(car1, car2)[m
