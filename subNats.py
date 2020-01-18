import asyncio
from nats.aio.client import Client as NATS
import positionModel_pb2

async def example():
    nc = NATS()

    async def error_cb(e):
        print("error:", e)

    await nc.connect("nats://hackaz.modularminingcloud.com:4222",
                     user_credentials='./hack.creds', #hack.creds should probably be gitignored from the repo
                     error_cb=error_cb,
                     )

    future = asyncio.Future()

    async def message_handler(msg):
        nonlocal future
        future.set_result(msg)
        positionModel = positionModel_pb2.State()
        positionModel.ParseFromString(msg.data)
        print(positionModel)
        print("got one")


    sid = await nc.subscribe("single-scenario-easy-1", cb=message_handler)
    print("passed await")

    msg = await asyncio.wait_for(future, 1)
    await nc.auto_unsubscribe(sid, 3)
    print("passed unsubscribe")
    await nc.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
loop.close()
