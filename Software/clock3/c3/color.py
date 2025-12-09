import functools

class Color:
    def __init__(self,r,g,b):
        self.b = bytearray([r,g,b])

ROT = Color(255,0,0)
GRÜN = Color(0,255,0)
BLAU = Color(0,0,255)

def colors_bytes(cols):
    "Wandelt Liste von Color in bytearray um"
    return functools.reduce( lambda a,b: a+b.b, cols, bytearray([]))
