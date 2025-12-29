"""
Nimm shift-cmd-r/chromium oder option-cmd-r/safari, um Skripte ohne Cache neu zu laden
"""
import asyncio, json
from quart import Quart, render_template, websocket

from .broker import Broker
from .messages import MTYPES, MKEYS, msg_script_consts
from .controler import Controler

app = Quart(__name__)

broker = Broker()

@app.route('/')
async def index():
    return await render_template("q1.html",script_constants=msg_script_consts())

async def _receive() -> None:
    while True:
        message = await websocket.receive()
        d = json.loads(message)
        mtype = d[MKEYS.mtype.name]
        if mtype == MTYPES.STARTUP.name:
            # Startup message wird mit status beantwortet
            print("Handling startup")
        else:
            await con.handle_msg(message)
            #await broker.publish(message)
        # Erzeuge und publishe status-Nachricht
        a = con.status.msg_dict()
        a[MKEYS.mtype.name] = MTYPES.STATUS.name
        await broker.publish(json.dumps(a))

@app.websocket("/ws")
async def ws() -> None:
    task = None
    try:
        task = asyncio.ensure_future(_receive())
        async for message in broker.subscribe():
            await websocket.send(message)
    finally:
        if task:
            task.cancel()
            await task

async def stopper(t):
    count = 6
    while count > 0:
        await asyncio.sleep(10)
        print("stopper")
        count -= 1
    t.cancel()

con = Controler(broker)

async def main():
    t = asyncio.create_task(app.run_task())
    c = asyncio.create_task(con.run())
    #b = asyncio.create_task(broker.sender())
    #s = asyncio.create_task(stopper(t))
    try:
        await t
    except asyncio.CancelledError:
        print("app gestoppt")
    #c.cancel()
    #await s

if __name__ == "__main__":
    asyncio.run(main())
    print("Gestoppt")
