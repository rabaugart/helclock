#!/usr/bin/env python3

import c3, c3.gen, c3.hclock
from c3.generator import ColWortGenerator

s = c3.Spi()

SL = 110

#ca = c3.filled_color_array( [c3.ROT,c3.GRÜN,c3.BLAU], int(SL), c3.GRÜN )
ca = c3.filled_color_array( [c3.ROT,c3.GRÜN,c3.BLAU], int(SL/5), c3.BLAU )
#ca = ([c3.ROT,c3.GRÜN,c3.BLAU]+[c3.SCHWARZ]*2)*3
#ca = ([c3.GRÜN*0.3,c3.GRÜN,c3.GRÜN*0.3]+[c3.SCHWARZ]*2)*3

#s.putcolgen(c3.gen.rotate(ca),0.1)
#s.putcolgen(c3.hclock.zeit_spi_generator(),0.1)
s.putcolgen(ColWortGenerator(),0.1)
