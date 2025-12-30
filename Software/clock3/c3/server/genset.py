from .agenerator import AGenerator, ClockGen, TestGen
from .messages import MKEYS

class ConStatus:

    def __init__(self):
        self.generators = [
            AGenerator("A",ClockGen),
            AGenerator("B",ClockGen),
            AGenerator("C",TestGen),
        ]
        self._selected_generator = self.generators[0]

    def select_generator(self,gname):
        l = list( g
            for g in self.generators if g.name == gname )
        assert( len(l)== 1)
        self._selected_generator = l[0]

    def selected_generator(self):
        return self._selected_generator

    def set_sel_farbe(self,colsec,color,value):
        self._selected_generator.farbmap[colsec].set(color,value)

    def msg_dict(self):
        return {
            MKEYS.generators.name : list( i.msg_dict() for i in self.generators ),
            MKEYS.selected_generator.name: self._selected_generator.name,
        }

class ProdGenSet(ConStatus):

    def __init__(self):
        ConStatus.__init__(self)

class TestGenSet(ConStatus):

    def __init__(self):
        ConStatus.__init__(self)
