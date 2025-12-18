#!/usr/bin/env python3

import queue, time, threading

from flask import Flask

import c3, c3.gen

class Controler:
    def __init__(self):
        self.q = queue.Queue()
        self.run_flag = False
        self.generators = {
            "blau": c3.gen.rotate([c3.GRÜN,c3.BLAU,c3.BLAU]),
            "rot": c3.gen.rotate([c3.GRÜN,c3.ROT,c3.ROT]),
            "gruen": c3.gen.rotate([c3.GRÜN,c3.ROT,c3.ROT]),
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

collist = "\n".join(f'<div><a href="/gen/{col}">{col}</a></div>' for col in con.generators.keys())
page = f"""
<html>
<body>
{collist}
</body>
</html>
    """
@app.route("/")
def hello():
    return page

@app.route("/gen/<gname>")
def gen(gname):
    con.put(gname)
    return page

if __name__ == "__main__":
    con_thread = threading.Thread(target=con.run)
    con_thread.start()
    app.run(host="0.0.0.0")
    con.stop()
    con_thread.join()
