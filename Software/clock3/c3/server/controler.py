import asyncio, json, itertools
from enum import Enum
import unittest


from .messages import MKEYS, MTYPES, COL_SECT
from c3.color import VORDEFINIERTE_FARBEN

class Controler:
    def __init__(self):
        self.status = ConStatus()
        self.msg_queue = asyncio.Queue()
        self.gen_no = 0

    async def handle_msg(self,m):
        await self.msg_queue.put(m)

    def status(self):
        return self.status

    def update_status(self,m):
        "Message erhalten -> Status ändern"
        try:
            d = json.loads(m)
            mtype = d[MKEYS.mtype.name]
            print(f"Received {mtype}: {d}")
            if mtype == MTYPES.GENERATOR_SELECT.name:
                try:
                    gname = d[MKEYS.selected_generator.name]
                    self.gen_no = list(i for (i,gi) in enumerate(self.status.generators)
                        if gi.name == gname)[0]
                    print(f"Neuer Generator {gname}/{self.gen_no}")
                except Exception as e:
                    print(f"Error {e}")
                    self.gen_no = 0
            else:
                print(f"Received unhandled {d}")
        except Exception as e:
            print(f"Error {e}")
            self.gen_no = 0

    async def run(self):
        running = True
        while running:
            print(f"Using {self.gen_no}")
            async for f in self.status.generators[self.gen_no]:
                print("Controler",f)
                try:
                    m = self.msg_queue.get_nowait()
                    print(f"Queue: {m}")
                    self.update_status(m)
                    break
                except asyncio.QueueEmpty:
                    pass
            else:
                running = False

GENERATOR_TYPE = Enum("PT","Uhr Test")

GENTYPE_COLMAP = {
    GENERATOR_TYPE.Uhr : [COL_SECT.Vordergrund,COL_SECT.Hintergrund],
    GENERATOR_TYPE.Test : [COL_SECT.Vordergrund,COL_SECT.Mittelfarbe,COL_SECT.Hintergrund],
}

class AGenerator(dict):
    "Async generator"

    INIT = itertools.cycle(VORDEFINIERTE_FARBEN)

    def __init__(self,name,gent):
        self.name = name
        self.generator_type = gent
        self.count = 0
        self.farbmap = dict(zip( GENTYPE_COLMAP[self.generator_type], self.INIT))

    def msg_dict(self):
        return {
            MKEYS.generator_name.name : self.name,
            MKEYS.generator_type.name : self.generator_type.name,
            MKEYS.colors.name : dict( (si.name,ci.msg_dict()) for (si,ci) in self.farbmap.items()),
        }

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            await asyncio.sleep(5)
        except asyncio.CancelledError:
            raise StopAsyncIteration
        self.count += 1
        return f"{self.name} Farbe {self.count}"

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
