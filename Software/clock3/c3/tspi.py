from .spibase import SpiBase

class Spi(SpiBase):
    def __init__(self):
        self.bs = []
    def putbytes(self,b):
        if len(self.bs) < 1000:
            self.bs.append( b )
