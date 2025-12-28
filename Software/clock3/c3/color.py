import functools, itertools
from enum import Enum

RGB = Enum("RGB","rot grün blau")

class Color:
    def __init__(self,r,g,b):
        self.b = bytearray([r,g,b])
    def __eq__(self,o):
        if isinstance(o,Color):
            return self.b == o.b
        return False
    def __mul__(self,fac):
        nfac = max(min(float(fac),1.0),0.0)
        return Color(*list(int(i*nfac) for i in self.b))
    def __hash__(self):
        return hash(self.b.hex())
    def msg_dict(self):
        return {
            RGB.rot.name: self.b[0],
            RGB.grün.name: self.b[1],
            RGB.blau.name: self.b[2],
        }


ROT = Color(255,0,0)
GRÜN = Color(0,255,0)
BLAU = Color(0,0,255)
GELB = Color(255,255,0)
WEISS = Color(255,255,255)
LILA = Color(255,0,255)
SCHWARZ = Color(0,0,0)

VORDEFINIERTE_FARBEN = [ROT,GRÜN,BLAU,LILA,GELB]

def colors_bytes(cols):
    "Wandelt Liste von Color in bytearray um"
    return functools.reduce( lambda a,b: a+b.b, cols, bytearray([]))

def filled_color_array(cols,le,fillcolor=SCHWARZ):
    "Fülle mit fillcolor bis zur Länge le auf"
    return cols + [fillcolor]*(le-len(cols))
