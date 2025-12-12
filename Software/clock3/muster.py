#!/usr/bin/env python3

import time, sys
import c3, c3.gen

s = c3.Spi()

SL = 15

ca = c3.filled_color_array( [c3.ROT,c3.GRÜN,c3.BLAU], SL )
ca = ([c3.ROT,c3.GRÜN,c3.BLAU]+[c3.SCHWARZ]*2)*3
#ca = ([c3.GRÜN*0.3,c3.GRÜN,c3.GRÜN*0.3]+[c3.SCHWARZ]*2)*3

s.putcolgen(c3.gen.blink(ca),0.3)
