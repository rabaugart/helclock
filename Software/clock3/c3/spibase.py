import datetime, time
from .color import colors_bytes
from .ternär import time_ternär_colors

class SpiBase:

    def putcolors(self,cl):
        "Gebe Liste von Color aus"
        self.putbytes(colors_bytes(cl))

    def puttime(self,ti=None):
        t = ti if ti else datetime.datetime.now().time()
        self.putcolors(time_ternär_colors(t))

    def putcolgen(self,it,sleep=1.0):
        "Gib Generator aus, der Listen von Color erzeugt"
        for i in it:
            self.putcolors(i)
            time.sleep(sleep)

    def putbytes(self,b):
        raise NotImplementedError
