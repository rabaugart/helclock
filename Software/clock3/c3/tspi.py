from .spibase import SpiBase

class Spi(SpiBase):
    def __init__(self):
        self.b = None
    def putbytes(self,b):
        self.b = b
