import asyncio
from nats.aio.client import Client as NATS
import positionModel_pb2
import time
import sys
import requests
from python.car_modeling.Car import *

scenarios = []
scenarios.append("single-scenario-easy-1")
scenarios.append("single-scenario-easy-2")
scenarios.append("single-scenario-easy-3")
scenarios.append("multiple-scenarios-1")
scenarios.append("multiple-scenarios-2")
scenarios.append("multiple-scenarios-3")


def alert_json(data, alertID, region):
    print("Current Scenario: " + str(curr_scenario))
    return ({"alarmId": "placeholder",
             "streamId": scenarios[curr_scenario],
             "sourceId": "20c067e529874f56a57d0022f64cc74e",
             "type": alertID,
             "region": region,
             "position": {
                 "latitude": data.positionModel.OwnPosition.Latitude,
                 "longitude": data.positionModel.OwnPosition.Longitude,
                 "altitude": data.positionModel.OwnPosition.Altitude,
                 "heading": data.positionModel.OwnPosition.Heading,
                 "velocity": data.positionModel.OwnPosition.Velocity
             },
             "target1Position": {
                 "latitude": data.positionModel.Target1Position.Latitude,
                 "longitude": data.positionModel.Target1Position.Longitude,
                 "altitude": data.positionModel.Target1Position.Altitude,
                 "heading": data.positionModel.Target1Position.Heading,
                 "velocity": data.positionModel.Target1Position.Velocity
             },
             "target2Position": {
                 "latitude": data.positionModel.Target2Position.Latitude,
                 "longitude": data.positionModel.Target2Position.Longitude,
                 "altitude": data.positionModel.Target2Position.Altitude,
                 "heading": data.positionModel.Target2Position.Heading,
                 "velocity": data.positionModel.Target2Position.Velocity
             },
             "target3Position":{
                 "latitude": data.positionModel.Target3Position.Latitude,
                 "longitude": data.positionModel.Target3Position.Longitude,
                 "altitude": data.positionModel.Target3Position.Altitude,
                 "heading": data.positionModel.Target3Position.Heading,
                 "velocity": data.positionModel.Target3Position.Velocity
             }
             })

class DataPoints:
    def __init__(self, positionmodel, timestamp):
        self.positionModel = positionmodel
        self.timestamp = timestamp
    def string_json(self, return_list, alert_list):
        return ({"timestamp": self.timestamp,
		"position_data": [
			{"latitude": self.positionModel.OwnPosition.Latitude, "longitude": self.positionModel.OwnPosition.Longitude, "altitude": self.positionModel.OwnPosition.Altitude,"heading": self.positionModel.OwnPosition.Heading, "velocity": self.positionModel.OwnPosition.Velocity},
			{"latitude": self.positionModel.Target1Position.Latitude,"longitude": self.positionModel.Target1Position.Longitude,"altitude": self.positionModel.Target1Position.Altitude,"heading": self.positionModel.Target1Position.Heading, "velocity": self.positionModel.Target1Position.Velocity},
			{"latitude": self.positionModel.Target2Position.Latitude,"longitude": self.positionModel.Target2Position.Longitude,"altitude": self.positionModel.Target2Position.Altitude,"heading": self.positionModel.Target2Position.Heading, "velocity": self.positionModel.Target2Position.Velocity},
			{"latitude": self.positionModel.Target3Position.Latitude,"longitude": self.positionModel.Target3Position.Longitude,"altitude": self.positionModel.Target3Position.Altitude,"heading": self.positionModel.Target3Position.Heading, "velocity": self.positionModel.Target3Position.Velocity}
		],
        "prediction_data": [
            {
                "predictions": return_list
            }
        ],
        "alert_data": [
            {
                "alert_and_time": alert_list
            }
        ]
		})


async def run(loop, dataAddedCallback, curr_scenario):
    nc = NATS()
    async def error_cb(e):
        print("error:", e)
    print("Current Scenario: " + str(curr_scenario))
    await nc.connect("nats://hackaz.modularminingcloud.com:4222",
                     user_credentials='./hack.creds', #hack.creds should probably be gitignored from the repo
                     error_cb=error_cb,
                     io_loop=loop,
                     )

    messages_received = 0
    positionList = []
    async def message_handler(msg):
        future_list = []
        alert_list = []
        # file = open("pos_data.txt", "a")
        positionModel = positionModel_pb2.State()
        positionModel.ParseFromString(msg.data)
        # print(positionModel)
        # file.write("")
        # file.write(str(positionModel))
        timestamp = time.time()
        # file.write(str(timestamp))
        # file.write("\n")
        # file.write("&\n")
        # file.close()
        newdata = DataPoints(positionModel, timestamp)
        future_list, alert_list = dataAddedCallback(newdata)
        positionList.append(newdata)
        # outfile = open("pos_data_json.txt", "w")
        # outfile.write(DataPoints(positionModel, timestamp).to_json())
        # outfile.close()
        # car1 = Car(newdata.positionModel.OwnPosition.Latitude, newdata.positionModel.OwnPosition.Longitude,
        #            newdata.positionModel.OwnPosition.Heading, newdata.positionModel.OwnPosition.Velocity)
        # car2 = Car(newdata.positionModel.Target1Position.Latitude, newdata.positionModel.Target1Position.Longitude,
        #            newdata.positionModel.Target1Position.Heading, newdata.positionModel.Target1Position.Velocity)
        # car1.predict_collision(car1, car2)
        nonlocal messages_received
        messages_received += 1
        if messages_received % 15 == 0:
            x = alert_json(newdata,1,1)
            p = requests.post(url="https://hackaz.modularminingcloud.com/api/Alert", json=x)
            #print("posted")
        print(messages_received)
        print(positionModel)
        r = requests.post(url="http://localhost:9190/data", json=newdata.string_json(future_list, alert_list))
        #print(messages_received)
        print(r.text)

    
    sid = await nc.subscribe(scenarios[curr_scenario], cb=message_handler)
    print("Current Scenario: " + str(curr_scenario))	

    await asyncio.sleep(1)

def initPosCollection(dataAddedCallback, x):
    debug_mode = True
    curr_scenario = -1

    curr_scenario = x
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(run(loop, dataAddedCallback, curr_scenario))
    loop.run_forever()
