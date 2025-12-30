"""
Nimm shift-cmd-r/chromium oder option-cmd-r/safari, um Skripte ohne Cache neu zu laden
"""
import asyncio, platform
from quart import Quart, render_template, websocket

from .messages import msg_script_consts, Command
from .controler import Controler

app = Quart(__name__)

@app.route('/')
async def index():
    return await render_template("q1.html",script_constants=msg_script_consts())

async def _receive() -> None:
    while True:
        message = await websocket.receive()
        try:
            cmd = Command.parse_json(message)
            print("WS received", cmd)
            await con.handle_command(cmd)
        except Exception as e:
            print("Error ws receiving",e,message)

@app.websocket("/ws")
async def ws() -> None:
    task = None
    try:
        task = asyncio.ensure_future(_receive())
        async for message in con.subscribe():
            await websocket.send(message)
    finally:
        if task:
            task.cancel()
            await task

async def stopper():
    await asyncio.sleep(60*60)
    return True

con = Controler()

async def main():
    host = "127.0.0.1" if platform.system() == "Darwin" else "0.0.0.0"
    t = asyncio.create_task(app.run_task(host=host,shutdown_trigger=stopper))
    c = asyncio.create_task(con.run())
    await t
    print("Webserver gestoppt")
    await c
    #c.cancel()
    #await s

if __name__ == "__main__":
    asyncio.run(main())
    print("Gestoppt")
