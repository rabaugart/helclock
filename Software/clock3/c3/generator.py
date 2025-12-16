
import datetime
import unittest

import c3.color as c
from .gen import take
from .hclock import index_range, zeit_satz, wort_indexe
from .xtra import dt_tagkatcols

class Strang(list):

    SLEN = len(list(index_range()))

    def __init__(self,leer_col=c.SCHWARZ):
        for i in range(self.SLEN):
            self.append(leer_col)

    def setze_wort_color(self,w,col):
        for k in wort_indexe(w)[1]:
            self[k] = col

class ColWortGenerator:

    BG_COLOR = c.SCHWARZ
    FG_COLOR = c.ROT

    def __iter__(self):
        dt = self.zeit()
        while True:
            s = Strang(self.BG_COLOR)
            self.fülle_xtra(dt,s)
            self.fülle_zeit(dt.time(),s)
            yield s

    def fülle_xtra(self,dt,st):
        "Extra Worte zur datetime dt"
        for wi,ci in dt_tagkatcols(dt):
            st.setze_wort_color(wi,ci)

    def fülle_zeit(self,ti,st):
        for wi in zeit_satz(ti):
            st.setze_wort_color(wi,self.zwort_color(wi))

    def zwort_color(self,w):
        return ColWortGenerator.FG_COLOR

    def zeit(self):
        return datetime.datetime.now()

class TestGenerator(ColWortGenerator):
    def __init__(self,dt):
        self.dt = dt
    def zeit(self):
        return self.dt

class TestGen(unittest.TestCase):

    def testStrang(self):
        s = Strang()
        self.assertEqual(len(s),Strang.SLEN)
    def testGen1(self):
        g = ColWortGenerator()
        cl = list(take(g,1))[0]
        self.assertEqual(len(cl),Strang.SLEN)
        self.assertEqual(set(cl),set([ColWortGenerator.FG_COLOR,ColWortGenerator.BG_COLOR]))
        # Hört mit ES IST ... auf
        self.assertEqual(cl[-1],ColWortGenerator.FG_COLOR)
        # Mehr als ES IST...
        self.assertGreater(cl.count(ColWortGenerator.FG_COLOR),5)
    def testXtra1(self):
        g = TestGenerator(datetime.datetime.fromisoformat("2025-01-06T12:00:00"))
        cl = list(take(g,1))[0]
        self.assertEqual(len(cl),Strang.SLEN)
        self.assertEqual(set(cl),set([ColWortGenerator.FG_COLOR,ColWortGenerator.BG_COLOR,c.LILA]))
        self.assertEqual(cl.count(c.LILA),3)
    def testXtra2(self):
        g = TestGenerator(datetime.datetime.fromisoformat("2025-01-07T12:00:00"))
        cl = list(take(g,1))[0]
        self.assertEqual(set(cl),set([ColWortGenerator.FG_COLOR,ColWortGenerator.BG_COLOR]))
