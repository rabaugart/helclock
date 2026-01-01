import asyncio, itertools
from enum import Enum

from .messages import MKEYS, COL_SECT
from c3.color import VORDEFINIERTE_FARBEN, colors_bytes
from c3.gen import rotate_list
from c3.generator import ColWortGenerator

class ClockGen:
    TNAME = "clock"
    TCOL_SECTS = [COL_SECT.Vordergrund,COL_SECT.Hintergrund,COL_SECT.FeierVordergrund]

    def __init__(self,farbmap):
        self.farbmap = farbmap

    def gen(self):
        count = 0
        g = ColWortGenerator(fg=self.farbmap[COL_SECT.Vordergrund],
            bg=self.farbmap[COL_SECT.Hintergrund])
        print(f"Starting {g}")
        for i in g:
            yield colors_bytes(i), 0.1 if count < 1 else 5.0
            count += 1

class TestGen1:
    TNAME = "tgen1"
    TCOL_SECTS = [COL_SECT.Vordergrund,COL_SECT.Hintergrund]

    def __init__(self,farbmap,**kwds):
        self.farbmap = farbmap

    def gen(self):
        count = 0
        while True:
            yield colors_bytes([
                self.farbmap[COL_SECT.Vordergrund],
                self.farbmap[COL_SECT.Hintergrund],
                self.farbmap[COL_SECT.Vordergrund]]), 0.1 if count < 1 else 5.0
            count += 1

class TestGen2:
    TNAME = "tgen2"
    TCOL_SECTS = [COL_SECT.Vordergrund,COL_SECT.Mittelfarbe,COL_SECT.Hintergrund]
    def __init__(self,farbmap,**kwds):
        self.farbmap = farbmap
        self.slen = kwds.get("slen",3)
        self.pnum = kwds.get("pnum",1)

    def gen(self):
        count = 0
        l = ([ self.farbmap[COL_SECT.Vordergrund],
            self.farbmap[COL_SECT.Mittelfarbe]]+
            [self.farbmap[COL_SECT.Hintergrund]]*(self.slen-2))*self.pnum
        print(f"Starte TestGen2 mit Länge {len(l)}")
        for i in [self.farbmap[COL_SECT.Vordergrund],
            self.farbmap[COL_SECT.Mittelfarbe],self.farbmap[COL_SECT.Hintergrund]]:
            yield colors_bytes([i]*self.slen),0.1 if count < 1 else 5.0
            count += 1
        while True:
            yield colors_bytes(l),0.3
            l = rotate_list(l)

class AGenerator(dict):
    "Async generator"

    INIT = itertools.cycle(VORDEFINIERTE_FARBEN)

    def __init__(self,name,genclass,**kwds):
        self.name = name
        self.genclass = genclass
        self.genargs = kwds
        self.farbmap = dict(zip( genclass.TCOL_SECTS, self.INIT))
        self.gen = None

    def msg_dict(self):
        return {
            MKEYS.generator_name.name : self.name,
            MKEYS.generator_type.name : self.genclass.TNAME,
            MKEYS.colors.name : dict( (si.name,ci.msg_dict()) for (si,ci) in self.farbmap.items()),
        }

    def __aiter__(self):
        self.gen = self.genclass(self.farbmap,**self.genargs).gen()
        return self

    async def __anext__(self):
        b,s = next(self.gen)
        try:
            await asyncio.sleep(s)
        except asyncio.CancelledError:
            raise StopAsyncIteration
        return b
