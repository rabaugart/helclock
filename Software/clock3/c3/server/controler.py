import sys, asyncio, json

from c3 import Spi
from .messages import MKEYS, MTYPES
from .broker import Broker
from .genset import GENSETS

DEFAULT_CONTEXT = "service"

class Controler:
    def __init__(self,genset,spi=None):
        self.broker = Broker()
        self.status = genset
        self.msg_queue = None
        self.spi = spi if spi else Spi()

    async def handle_command(self,cmd):
        await self.msg_queue.put(cmd)

    def process_command(self,cmd):
        try:
            if cmd.mtype == MTYPES.STARTUP:
                return
            self.status.select_generator( cmd.selected_generator)
            if cmd.mtype == MTYPES.COL_UPDATE:
                print("Setze Farbe:",cmd.selected_generator,cmd.colsec,cmd.color,cmd.value)
                self.status.set_sel_farbe(cmd.colsec,cmd.color,cmd.value)
        except Exception as e:
            print("Process error:",e)

    async def generate(self):
        print(f"Starting {self.status.selected_generator().name}/{self.status.selected_generator().name_typ()}")
        await self.publish_status()
        async for f in self.status.selected_generator():
            #print("Controler",f)
            self.spi.putbytes(f)
        print("Generator stopped")

    async def run(self):
        if not self.msg_queue:
            self.msg_queue = asyncio.Queue()
        running = True
        gentask = asyncio.create_task(self.generate())
        while running:
            try:
                cmd = await self.msg_queue.get()
                if gentask:
                    gentask.cancel()
                    await gentask
                self.process_command(cmd)
                gentask = asyncio.create_task(self.generate())
                self.msg_queue.task_done()
                #await self.update_status(m)
            except asyncio.CancelledError:
                print("Controler stopped")
                break
        try:
            await self.msg_queue.join()
        except asyncio.CancelledError:
            pass

    async def publish_status(self):
        d = self.status.msg_dict()
        d[MKEYS.mtype.name] = MTYPES.STATUS.name
        await self.broker.publish(json.dumps(d))

    async def subscribe(self):
        async for m in self.broker.subscribe():
            yield m

def controler_from_argv():
    ctx = DEFAULT_CONTEXT if len(sys.argv) < 2 else sys.argv[1]
    if not ctx in GENSETS:
        l = ", ".join(GENSETS.keys())
        raise RuntimeError(f"Unbekanter Kontext: {ctx}, verfügbar {l}")
    print(f"Verwende Kontext: {ctx}")
    return Controler(GENSETS[ctx]())
