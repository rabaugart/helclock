import json
from enum import Enum

import unittest

MTYPES = Enum("MT","STARTUP STATUS GENERATOR_SELECT COL_UPDATE")
MKEYS = Enum("MK","mtype selected_generator generators generator_name generator_type colors")

COL_SECT = Enum("CS","Vordergrund Hintergrund Mittelfarbe")

def mtypes_js():
    return "\n".join( f'const MT_{i.name} = "{i.name}";' for i in MTYPES)

def mkeys_js():
    return "\n".join( f'const MK_{i.name} = "{i.name}";' for i in MKEYS)

def msg_script_consts():
    return mtypes_js() + "\n" + mkeys_js()

class Command:

    def __init__(self):
        self.mtype = None
        self.selected_generator = None

    @staticmethod
    def parse_json(msg):
        d = json.loads(msg)
        cmd = Command()
        cmd.mtype = MTYPES[d[MKEYS.mtype.name]]
        cmd.selected_generator = d[MKEYS.selected_generator.name]
        return cmd

    @staticmethod
    def select_generator(gname):
        c = Command()
        c.mtype = MTYPES.GENERATOR_SELECT
        c.selected_generator = gname
        return c

    @staticmethod
    def startup():
        c = Command()
        c.mtype = MTYPES.STARTUP
        return c

    def json(self):
        return json.dumps({
            MKEYS.mtype.name: self.mtype.name,
            MKEYS.selected_generator.name: self.selected_generator,
        })

class MsgTest(unittest.TestCase):

    def testCommand(self):
        c = Command.parse_json('{ "mtype": "GENERATOR_SELECT", "selected_generator":"A"}')
        self.assertEqual(c.mtype, MTYPES.GENERATOR_SELECT)
        self.assertEqual(c.selected_generator,"A")
        j2 = Command.select_generator("X").json()
        c2 = Command.parse_json(j2)
        self.assertEqual(c2.selected_generator,"X")

    def testMT(self):
        self.assertEqual(mtypes_js(),"""const MT_STARTUP = "STARTUP";
const MT_STATUS = "STATUS";
const MT_GENERATOR_SELECT = "GENERATOR_SELECT";
const MT_COL_UPDATE = "COL_UPDATE";""")
        self.assertEqual(mkeys_js(),"""\
const MK_mtype = "mtype";
const MK_selected_generator = "selected_generator";
const MK_generators = "generators";
const MK_generator_name = "generator_name";
const MK_generator_type = "generator_type";
const MK_colors = "colors";""")
if __name__ == "__main__":
    unittest.main()
