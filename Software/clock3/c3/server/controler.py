import asyncio, json, itertools
from enum import Enum
import unittest


from c3 import Spi
from .messages import MKEYS, MTYPES, COL_SECT
from .broker import Broker
from c3.color import VORDEFINIERTE_FARBEN, colors_bytes

class Controler:
    def __init__(self,spi=None):
        self.broker = Broker()
        self.status = ConStatus()
        self.msg_queue = None
        self.gen_no = 0
        self.spi = spi if spi else Spi()

    async def handle_command(self,cmd):
        await self.msg_queue.put(cmd)

    def process_command(self,cmd):
        try:
            if cmd.mtype == MTYPES.STARTUP:
                return
            l = list( (i,g)
                for (i,g) in enumerate(self.status.generators) if g.name == cmd.selected_generator )
            assert( len(l)== 1)
            i,g = l[0]
            self.gen_no = i
            self.status.selected_generator = g.name
            if cmd.mtype == MTYPES.COL_UPDATE:
                print("Setze Farbe:",g.name,cmd.colsec,cmd.color,cmd.value)
                g.farbmap[cmd.colsec].set(cmd.color,cmd.value)
        except Exception as e:
            print("Process error:",e)

    def selected_generator(self):
        return self.status.generators[self.gen_no]

    async def generate(self):
        print(f"Starting {self.gen_no}")
        await self.publish_status()
        async for f in self.selected_generator():
            print("Controler",f)
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


GENERATOR_TYPE = Enum("PT","Uhr Test")

class ClockGen:
    def __init__(self,farbmap):
        self.farbmap = farbmap

    def gen(self):
        count = 0
        while True:
            yield colors_bytes([
                self.farbmap[COL_SECT.Vordergrund],
                self.farbmap[COL_SECT.Hintergrund],
                self.farbmap[COL_SECT.Vordergrund]]), 0.1 if count < 1 else 5.0
            count += 1

class TestGen:
    def __init__(self,farbmap):
        self.farbmap = farbmap

    def gen(self):
        count = 0
        while True:
            yield colors_bytes([
                self.farbmap[COL_SECT.Vordergrund],
                self.farbmap[COL_SECT.Mittelfarbe],
                self.farbmap[COL_SECT.Hintergrund]]),0.1 if count < 1 else 5.0
            count += 1

GENTYPE_COLMAP = {
    GENERATOR_TYPE.Uhr : ([COL_SECT.Vordergrund,COL_SECT.Hintergrund],ClockGen),
    GENERATOR_TYPE.Test : ([COL_SECT.Vordergrund,COL_SECT.Mittelfarbe,COL_SECT.Hintergrund],TestGen),
}

class AGenerator(dict):
    "Async generator"

    INIT = itertools.cycle(VORDEFINIERTE_FARBEN)

    def __init__(self,name,gent):
        self.name = name
        self.generator_type = gent
        cols,genclass = GENTYPE_COLMAP[self.generator_type]
        self.farbmap = dict(zip( cols, self.INIT))
        self.genclass = genclass
        self.gen = None

    def msg_dict(self):
        return {
            MKEYS.generator_name.name : self.name,
            MKEYS.generator_type.name : self.generator_type.name,
            MKEYS.colors.name : dict( (si.name,ci.msg_dict()) for (si,ci) in self.farbmap.items()),
        }

    def __aiter__(self):
        self.gen = self.genclass(self.farbmap).gen()
        return self

    async def __anext__(self):
        b,s = next(self.gen)
        try:
            await asyncio.sleep(s)
        except asyncio.CancelledError:
            raise StopAsyncIteration
        return b

class ConStatus:

    def __init__(self):
        self.generators = [
            AGenerator("A",GENERATOR_TYPE.Uhr),
            AGenerator("B",GENERATOR_TYPE.Uhr),
            AGenerator("C",GENERATOR_TYPE.Test),
        ]
        self.selected_generator = self.generators[0].name

    def msg_dict(self):
        return {
            MKEYS.generators.name : list( i.msg_dict() for i in self.generators ),
            MKEYS.selected_generator.name: self.selected_generator,
        }

class ConTest(unittest.TestCase):

    def testMsg(self):
        c = ConStatus()
        ks = c.msg_dict().keys()
        self.assertIn(MKEYS.generators.name, ks)
        self.assertIn(MKEYS.selected_generator.name, ks)
        self.assertGreater( len(json.dumps(c.msg_dict())),50)
        #self.assertEqual(json.dumps(c.msg_dict()),"")
