
from enum import Enum

import unittest

MTYPES = Enum("MT","STARTUP STATUS GENERATOR_SELECT COL_UPDATE")
MKEYS = Enum("MK","mtype selected_generator generators generator_name generator_type colors")

def mtypes_js():
    return "\n".join( f'const MT_{i.name} = "{i.name}";' for i in MTYPES)

def mkeys_js():
    return "\n".join( f'const MK_{i.name} = "{i.name}";' for i in MKEYS)

def msg_script_consts():
    return mtypes_js() + "\n" + mkeys_js()

class MsgTest(unittest.TestCase):

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
