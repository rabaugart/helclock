from enum import Enum
import unittest
import datetime

# Extra Worte, zusätzlich zur Uhrzeit
XW = Enum("XW","B BE SO DOM HEL RA F")

TagKat = Enum("TagKat", "Normal Feiertag FamGeburtstag BekGeburtstag")

TagKatMap = {
    (1,6) : ([XW.DOM], TagKat.FamGeburtstag),
    (1,31) : ([XW.BE,XW.SO], TagKat.FamGeburtstag),
    (2,14) : ([XW.RA], TagKat.FamGeburtstag),
    (2,21) : ([XW.RA], TagKat.BekGeburtstag),
    (6,14) : ([XW.HEL], TagKat.FamGeburtstag),
}

def dt_tagkatlist(dt):
    return TagKatMap.get((dt.month,dt.day),None)

class XWTest(unittest.TestCase):
    def testSatz(self):
        dt = datetime.datetime.fromisoformat("2025-01-06 12:00:00")
        self.assertEqual(dt_tagkatlist(dt),TagKatMap[(1,6)])
        dt = datetime.datetime.fromisoformat("2025-01-07 12:00:00")
        self.assertEqual(dt_tagkatlist(dt),None)
