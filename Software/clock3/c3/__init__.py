from .color import *

from .ternär import *

try:
    from .spi import Spi
    HAS_SPI = True
except:
    from .tspi import Spi
    HAS_SPI = False

from .hclock import TEXT
