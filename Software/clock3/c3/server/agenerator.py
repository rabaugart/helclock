import asyncio, itertools

from .messages import MKEYS, COL_SECT
from c3.color import VORDEFINIERTE_FARBEN, colors_bytes
from c3.gen import rotate_list
from c3.generator import ColWortGenerator

class ClockGen:
    TNAME = "clock"
    TCOL_SECTS = [COL_SECT.Vordergrund,COL_SECT.Hintergrund,
        COL_SECT.FeierVordergrund,COL_SECT.FeierFam,COL_SECT.FeierHintergrund]

    def __init__(self,farbmap):
        self.farbmap = farbmap

    def gen(self):
        g = ColWortGenerator(
            fg=self.farbmap[COL_SECT.Vordergrund],
            bg=self.farbmap[COL_SECT.Hintergrund],
            ffg=self.farbmap[COL_SECT.FeierVordergrund],
            fbg=self.farbmap[COL_SECT.FeierHintergrund],
            sfg=self.farbmap[COL_SECT.FeierFam]
        )
        print(f"Starting {g}")
        yield colors_bytes(g.feier_demo()), 0.1
        for i in g:
            yield colors_bytes(i), 5.0

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
            yield colors_bytes([i]*self.slen*self.pnum),0.1 if count < 1 else 5.0
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

    def name_typ(self):
        return self.genclass.TNAME

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
