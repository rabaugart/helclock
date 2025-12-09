import datetime
from .color import colors_bytes
from .ternär import time_ternär_colors

class SpiBase:

    def putcolors(self,cl):
        self.putbytes(colors_bytes(cl))

    def puttime(self,ti=None):
        t = ti if ti else datetime.datetime.now().time()
        self.putcolors(time_ternär_colors(t))

    def putbytes(self,b):
        raise NotImplementedError
