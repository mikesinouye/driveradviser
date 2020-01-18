import asyncio
from nats.aio.client import Client as NATS
import positionModel_pb2

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
    async def message_handler(msg):
        file = open("pos_data.txt", "a")
        positionModel = positionModel_pb2.State()
        positionModel.ParseFromString(msg.data)
        print(positionModel)
        file.write("")
        file.write(str(positionModel))
        file.write("&\n")
        file.close()
        nonlocal messages_received
        messages_received += 1
        print(messages_received)


    sid = await nc.subscribe("multiple-scenarios-1", cb=message_handler)
    print("passed await")

    await asyncio.sleep(1)

def initPosCollection(positionList, dataAddedCallback):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.run_forever()
