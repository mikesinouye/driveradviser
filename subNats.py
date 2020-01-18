import asyncio
from nats.aio.client import Client as NATS
import positionModel_pb2
import time

import json

class DataPoints:
    def __init__(self, positionmodel, timestamp):
        self.positionModel = positionmodel
        self.timestamp = timestamp

async def run(loop):
    nc = NATS()

    async def error_cb(e):
        print("error:", e)

    await nc.connect("nats://hackaz.modularminingcloud.com:4222",
                     user_credentials='./hack.creds', #hack.creds should probably be gitignored from the repo
                     error_cb=error_cb,
                     io_loop=loop,
                     )

    messages_received = 0
    positionList = []
    async def message_handler(msg):
        file = open("pos_data.txt", "a")
        positionModel = positionModel_pb2.State()
        positionModel.ParseFromString(msg.data)
        print(positionModel)
        file.write("")
        file.write(str(positionModel))
        timestamp = time.time_ns()
        file.write(str(timestamp))
        file.write("\n")
        file.write("&\n")
        file.close()
        positionList.append(DataPoints(positionModel, timestamp))
        with open("pos_data_json.txt", "a") as outfile:
            json.dump(positionlist, outfile)
        outfile.close()
        nonlocal messages_received
        messages_received += 1
        print(messages_received)


    sid = await nc.subscribe("multiple-scenarios-1", cb=message_handler)
    print("passed await")

    await asyncio.sleep(1)

loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))
loop.run_forever()
