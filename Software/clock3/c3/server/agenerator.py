import asyncio, itertools
from enum import Enum

from .messages import MKEYS, COL_SECT
from c3.color import VORDEFINIERTE_FARBEN, colors_bytes
from c3.gen import rotate_list

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
        l = [ self.farbmap[COL_SECT.Vordergrund],
            self.farbmap[COL_SECT.Mittelfarbe],
            self.farbmap[COL_SECT.Hintergrund]]
        while True:
            yield colors_bytes(l),0.1 if count < 1 else 1.0
            l = rotate_list(l)
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
