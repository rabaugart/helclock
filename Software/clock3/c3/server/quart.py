import asyncio
from quart import Quart, render_template, websocket

from .broker import Broker

app = Quart(__name__)

broker = Broker()

@app.route('/')
async def index():
    return await render_template("q1.html")

async def _receive() -> None:
    while True:
        message = await websocket.receive()
        await broker.publish(message)

@app.websocket("/ws")
async def ws() -> None:
    try:
        task = asyncio.ensure_future(_receive())
        async for message in broker.subscribe():
            await websocket.send(message)
    finally:
        task.cancel()
        await task

if __name__ == "__main__":
    app.run()
