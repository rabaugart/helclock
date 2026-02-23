import json
from pathlib import Path
from .agenerator import AGenerator, ClockGen, TestGen1, TestGen2
from .messages import MKEYS

SERIALIZATION_FNAME = Path.home() / ".helclock"
class GenSetBase:

    def __init__(self):
        self.generators = []
        self._selected_generator = None
        self.serial_fname = None
        self.serial_fname = SERIALIZATION_FNAME

    def select_generator(self,gname):
        l = list( g
            for g in self.generators if g.name == gname )
        assert( len(l)== 1)
        self._selected_generator = l[0]
        self.fserialize()

    def selected_generator(self):
        if self._selected_generator is None:
            self._selected_generator = self.generators[0]
        return self._selected_generator

    def set_sel_farbe(self,colsec,color,value):
        self._selected_generator.farbmap[colsec].set(color,value)
        self.fserialize()

    def fserialize(self):
        try:
            if self.serial_fname:
                print(f"Serialisiere nach {self.serial_fname}")
                with open(self.serial_fname,"w") as f:
                    f.write(self.serialize())
        except Exception as e:
            print(f"Fehler beim Serialisieren {e}")

    def fdserialize(self):
        if self.serial_fname:
            try:
                print(f"Deserialisiere von {self.serial_fname}")
                with open(self.serial_fname,"r") as f:
                    self.deserialize(f.read())
            except Exception as e:
                print(f"Fehler beim Deserialisieren {e}")

    def serialize(self):
        d = {"selected":self.selected_generator().name}
        for gi in self.generators:
            gi.serialize(d)
        return json.dumps(d,indent=2)

    def deserialize(self,js):
        sd = json.loads(js)
        for gi in self.generators:
            gi.deserialize(sd)
        self.select_generator(sd["selected"])

    def msg_dict(self):
        return {
            MKEYS.generators.name : list( i.msg_dict() for i in self.generators ),
            MKEYS.selected_generator.name: self.selected_generator().name,
        }

class ProdGenSet(GenSetBase):

    def __init__(self,zeige_minuten):
        GenSetBase.__init__(self)
        from c3 import aktiviere_minutenanzeige
        aktiviere_minutenanzeige(zeige_minuten)
        print("Mit" if zeige_minuten else "Ohne","Minutenanzeige")
        self.generators = [
            AGenerator("Clock A",ClockGen),
            AGenerator("Clock B",ClockGen),
            AGenerator("Clock C",ClockGen),
            AGenerator("Test",TestGen2,slen=22,pnum=5),
        ]
        self._selected_generator = self.generators[0]
        self.fdserialize()

class TestGenSet(GenSetBase):
    "Test-Generator für unittests"

    def __init__(self,slen=3):
        GenSetBase.__init__(self)
        self.generators = [
            AGenerator("A",TestGen1),
            AGenerator("B",TestGen1),
            AGenerator("C",TestGen2,slen=slen),
        ]
        self.fdserialize()

GENSETS = {
    "service_min": lambda:ProdGenSet(True),
    "service": lambda:ProdGenSet(False),
    "testservice": TestGenSet,
}
