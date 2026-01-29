import unittest
import datetime

from .worte import XW, TagKat
from .color import LILA

TagKatMap = {
    (1,6) : ([XW.DOM], TagKat.FamGeburtstag),
    (1,31) : ([XW.BE,XW.SO], TagKat.FamGeburtstag),
    (2,14) : ([XW.RA], TagKat.FamGeburtstag),
    (2,21) : ([XW.RA], TagKat.BekGeburtstag),
    (6,14) : ([XW.HEL], TagKat.FamGeburtstag),
}

TagKatColors = {
    TagKat.Feiertag : LILA,
    TagKat.FamGeburtstag : LILA,
    TagKat.BekGeburtstag : LILA,
}

def dt_tagkat(dt):
    return TagKatMap.get((dt.month,dt.day),None)

def dt_tagkatcols(dt,map=TagKatColors):
    "[(xw1,col1),(xw2,col2),...] ggf. leer"
    ws_tka = dt_tagkat(dt)
    if not ws_tka:
        return []
    ws, tkat = ws_tka
    col = map.get(tkat,None)
    return list( (wi,col) for wi in ws ) if col else []

class XWTest(unittest.TestCase):
    def testSatz(self):
        dt = datetime.datetime.fromisoformat("2025-01-06 12:00:00")
        self.assertEqual(dt_tagkat(dt),TagKatMap[(1,6)])
        self.assertEqual(dt_tagkatcols(dt),[(XW.DOM,LILA)])
        dt = datetime.datetime.fromisoformat("2025-01-07 12:00:00")
        self.assertEqual(dt_tagkat(dt),None)
        self.assertEqual(dt_tagkatcols(dt),[])
