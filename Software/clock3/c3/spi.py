import spidev
from .spibase import SpiBase

class Spi(SpiBase):
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.spi.max_speed_hz = 2000000

    def putbytes(self,b):
        self.spi.writebytes(b)
