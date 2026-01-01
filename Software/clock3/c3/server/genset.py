from .agenerator import AGenerator, ClockGen, TestGen1, TestGen2
from .messages import MKEYS

class GenSetBase:

    def __init__(self):
        self.generators = []
        self._selected_generator = None

    def select_generator(self,gname):
        l = list( g
            for g in self.generators if g.name == gname )
        assert( len(l)== 1)
        self._selected_generator = l[0]

    def selected_generator(self):
        if self._selected_generator is None:
            self._selected_generator = self.generators[0]
        return self._selected_generator

    def set_sel_farbe(self,colsec,color,value):
        self._selected_generator.farbmap[colsec].set(color,value)

    def msg_dict(self):
        return {
            MKEYS.generators.name : list( i.msg_dict() for i in self.generators ),
            MKEYS.selected_generator.name: self.selected_generator().name,
        }

class ProdGenSet(GenSetBase):

    def __init__(self):
        GenSetBase.__init__(self)
        self.generators = [
            AGenerator("Clock A",ClockGen),
            AGenerator("Clock B",ClockGen),
            AGenerator("Test",TestGen2),
        ]
        self._selected_generator = self.generators[0]

class TestGenSet(GenSetBase):
    "Test-Generator für unittests"

    def __init__(self,slen=3):
        GenSetBase.__init__(self)
        self.generators = [
            AGenerator("A",TestGen1),
            AGenerator("B",TestGen1),
            AGenerator("C",TestGen2,slen=slen),
        ]
