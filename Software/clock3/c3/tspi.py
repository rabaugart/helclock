from .spibase import SpiBase

class Spi(SpiBase):
    def __init__(self):
        self.bs = []
    def putbytes(self,b):
        self.bs.append( b )
