
import datetime
import unittest

import c3.color as c
from .gen import take
from .hclock import index_range, zeit_satz, wort_indexe
from .xtra import dt_tagkatcols, dt_tagkat, TagKat, XW
from .worte import MIW, zeige_minuten

class Strang(list):

    SLEN = len(list(index_range()))

    def __init__(self,leer_col=c.SCHWARZ):
        for i in range(self.SLEN):
            self.append(leer_col)

    def setze_wort_color(self,w,col):
        for k in wort_indexe(w)[1]:
            self[k] = col

class ColWortGenerator:

    BG_COLOR = c.GRÜN*0.1
    FG_COLOR = c.ROT
    FFG_COLOR = c.WEISS
    FBG_COLOR = c.SCHWARZ
    SFG_COLOR = c.LILA

    def __init__(self,**kwlist):
        self.bg = kwlist.get("bg",self.BG_COLOR)
        self.fg = kwlist.get("fg",self.FG_COLOR)
        # Feitertage
        self.ffg = kwlist.get("ffg",self.FFG_COLOR)
        self.fbg = kwlist.get("fbg",self.FBG_COLOR)
        # Die Sonderzeichen
        self.sfg = kwlist.get("sfg",self.SFG_COLOR)
        # Für alle TagKat-Kategorien wird ffg verwendet
        self.tagkat_map = { k:self.sfg for k in TagKat}

    def __iter__(self):
        while True:
            dt = self.zeit()
            tkat = dt_tagkat(dt)
            s = Strang(self.fbg if tkat else self.bg)
            self.fülle_xtra(dt,s)
            self.fülle_zeit(dt.time(),tkat,s)
            yield s

    def fülle_xtra(self,dt,st):
        "Extra Worte zur datetime dt"
        for wi,ci in dt_tagkatcols(dt,self.tagkat_map):
            st.setze_wort_color(wi,ci)

    def fülle_zeit(self,ti,tkat,st):
        for wi in zeit_satz(ti,True):
            st.setze_wort_color(wi,self.zwort_color(wi,tkat))
        if not zeige_minuten():
            st.setze_wort_color(MIW.M4,c.SCHWARZ)

    def zwort_color(self,w,tkat):
        return self.ffg if tkat else self.fg

    def feier_demo(self):
        "Erzeuge Strang mit Zeitwörtern um 12:16 und X-Wörtern in Feiertagsfarben"
        st = Strang(self.fbg)
        for wi in zeit_satz(self.zeit()):
            st.setze_wort_color(wi,self.ffg)
        for xwi in XW:
            st.setze_wort_color(xwi,self.sfg)
        return st

    def zeit(self):
        return datetime.datetime.now()

    def __str__(self):
        return f"ClockGen fg:{self.fg}, bg: {self.bg}, ffg: {self.ffg}, sfg: {self.sfg}, fbg: {self.fbg}"

class TestGenerator(ColWortGenerator):
    def __init__(self,dt):
        ColWortGenerator.__init__(self)
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
        # Hört mit ES IST ... auf (vor den 4 Minuten LEDs)
        self.assertEqual(cl[-5],ColWortGenerator.FG_COLOR)
        # Mehr als ES IST...
        self.assertGreater(cl.count(ColWortGenerator.FG_COLOR),5)
    def testXtra1(self):
        g = TestGenerator(datetime.datetime.fromisoformat("2025-01-06T12:00:00"))
        cl = list(take(g,1))[0]
        self.assertEqual(len(cl),Strang.SLEN)
        self.assertEqual(set(cl),set([ColWortGenerator.FFG_COLOR,ColWortGenerator.FBG_COLOR,ColWortGenerator.SFG_COLOR]))
        self.assertEqual(cl.count(c.LILA),3)
        self.assertEqual(set(g.feier_demo()),set([ColWortGenerator.FFG_COLOR,ColWortGenerator.FBG_COLOR,ColWortGenerator.SFG_COLOR]))
    def testXtra2(self):
        g = TestGenerator(datetime.datetime.fromisoformat("2025-01-07T12:00:00"))
        cl = list(take(g,1))[0]
        self.assertEqual(set(cl),set([ColWortGenerator.FG_COLOR,ColWortGenerator.BG_COLOR]))
