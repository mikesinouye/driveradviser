import asyncio
from nats.aio.client import Client as NATS
import positionModel_pb2
import time
import sys
import requests
from python.car_modeling.Car import *


debug_mode = True

class DataPoints:
    def __init__(self, positionmodel, timestamp):
        self.positionModel = positionmodel
        self.timestamp = timestamp
    def string_json(self):
        return ({"timestamp": self.timestamp,
		"position_data": [
			{"latitude": self.positionModel.OwnPosition.Latitude, "longitude": self.positionModel.OwnPosition.Longitude, "altitude": self.positionModel.OwnPosition.Altitude,"heading": self.positionModel.OwnPosition.Altitude, "velocity": self.positionModel.OwnPosition.Velocity},
			{"latitude": self.positionModel.Target1Position.Latitude,"longitude": self.positionModel.Target1Position.Longitude,"altitude": self.positionModel.Target1Position.Altitude,"heading": self.positionModel.Target1Position.Heading, "velocity": self.positionModel.Target1Position.Velocity}, 
			{"latitude": self.positionModel.Target2Position.Latitude,"longitude": self.positionModel.Target2Position.Longitude,"altitude": self.positionModel.Target2Position.Altitude,"heading": self.positionModel.Target2Position.Heading, "velocity": self.positionModel.Target2Position.Velocity}, 
			{"latitude": self.positionModel.Target3Position.Latitude,"longitude": self.positionModel.Target3Position.Longitude,"altitude": self.positionModel.Target3Position.Altitude,"heading": self.positionModel.Target3Position.Heading, "velocity": self.positionModel.Target3Position.Velocity}
		]
		})

async def run(loop, dataAddedCallback):
    nc = NATS()

    async def error_cb(e):
        print("error:", e)

    await nc.connect("nats://hackaz.modularminingcloud.com:4222",
                     user_credentials='../hack.creds', #hack.creds should probably be gitignored from the repo
                     error_cb=error_cb,
                     io_loop=loop,
                     )

    messages_received = 0
    positionList = []
    async def message_handler(msg):
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
        dataAddedCallback(newdata)
        positionList.append(newdata)
        # outfile = open("pos_data_json.txt", "w")
        # outfile.write(DataPoints(positionModel, timestamp).to_json())
        # outfile.close()
        car1 = Car(newdata.positionModel.OwnPosition.Latitude, newdata.positionModel.OwnPosition.Longitude,
                   newdata.positionModel.OwnPosition.Heading, newdata.positionModel.OwnPosition.Velocity)
        car2 = Car(newdata.positionModel.Target1Position.Latitude, newdata.positionModel.Target1Position.Longitude,
                   newdata.positionModel.Target1Position.Heading, newdata.positionModel.Target1Position.Velocity)
        car1.predict_collision(car1,car2)
        nonlocal messages_received
        messages_received += 1
        r = requests.post(url="http://localhost:9190/data", json=newdata.string_json())
        # print(messages_received)


    sid = await nc.subscribe("multiple-scenarios-2", cb=message_handler)
    print("passed await")

    await asyncio.sleep(1)

def initPosCollection(dataAddedCallback):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop, dataAddedCallback))
    loop.run_forever()
