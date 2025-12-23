#!/usr/bin/env python3

import queue, time, threading

# Flask docs
# https://flask.palletsprojects.com/en/stable/
# oder auch Quart
# https://quart.palletsprojects.com/en/latest/
from flask import Flask
from flask.templating import render_template

import c3, c3.gen

# Konfiguration
WS_SERVER_PORT = 8764

class Controler:
    def __init__(self):
        self.q = queue.Queue()
        self.run_flag = False
        self.generators = {
            "blau": c3.gen.rotate([c3.GRÜN,c3.BLAU,c3.BLAU]),
            "rot/grün": c3.gen.rotate([c3.GRÜN,c3.ROT,c3.ROT]),
            "grün/rot": c3.gen.rotate([c3.GRÜN,c3.GRÜN,c3.ROT]),
        }
        self.spi = c3.Spi()

    def put(self,cmd):
        self.q.put(cmd)

    def stop(self):
        self.run_flag = False

    def run(self):
        self.run_flag = True
        cmd = "blau"
        while self.run_flag:
            gen = self.generators[cmd]
            for coli in gen:
                try:
                    cmd = self.q.get_nowait()
                    print(f"Received {cmd}")
                    break
                except queue.Empty:
                    pass
                #print(f"loop {cmd}, {coli}")
                self.spi.putcolors(coli)
                if not self.run_flag:
                    break
                time.sleep(0.3)
        print("Controler stopped")

con = Controler()
app = Flask(__name__)

COL_CONFIGS=con.generators.keys()

def render_main():
    return render_template("main.html",ws_server_port=WS_SERVER_PORT, colconfigs=COL_CONFIGS)

@app.route("/")
def hello():
    return render_main()

@app.route("/gen/<gname>")
def gen(gname):
    con.put(gname)
    return render_main()

import asyncio
#
# Docs zu websockets
# https://websockets.readthedocs.io/en/stable/
#
from websockets.asyncio.server import serve

async def echo(websocket):
    async for message in websocket:
        print(message)
        await websocket.send(message)

async def wsmain():
    # set this future to exit the server
    stop = asyncio.get_running_loop().create_future()
    async with serve(echo, "0.0.0.0", WS_SERVER_PORT) as server:
        await stop

if __name__ == "__main__":
    con_thread = threading.Thread(target=con.run)
    con_thread.start()

    ws_thread = threading.Thread(target=lambda:asyncio.run(wsmain()))
    ws_thread.start()

    app.run(host="0.0.0.0")
    con.stop()
    con_thread.join()
