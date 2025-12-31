import json
from enum import Enum

from c3.color import RGB

import unittest

MTYPES = Enum("MT","STARTUP STATUS GENERATOR_SELECT COL_UPDATE")
MKEYS = Enum("MK","mtype selected_generator generators generator_name generator_type colsec color value colors")

def mtypes_js():
    return "\n".join( f'const MT_{i.name} = "{i.name}";' for i in MTYPES)

def mkeys_js():
    return "\n".join( f'const MK_{i.name} = "{i.name}";' for i in MKEYS)

COL_SECT = Enum("CS","Vordergrund Hintergrund Mittelfarbe")

COL_SECT_TRANS = {
    COL_SECT.Mittelfarbe: "Mittl. Farbe",
}

def cs_trans(cs):
    return COL_SECT_TRANS.get(cs,cs.name)

def msg_col_sect_map():
    return "const cs_map = new Map();\n"+"\n".join(
        f'cs_map.set("{i.name}","{cs_trans(i)}");' for i in COL_SECT
    )

def msg_script_consts():
    return "\n".join( [mtypes_js(), mkeys_js(), msg_col_sect_map() ])

class Command:

    def __init__(self):
        self.mtype = None
        self.selected_generator = None
        self.colsec = None
        self.color = None
        self.value = None

    @staticmethod
    def parse_json(msg):
        d = json.loads(msg)
        cmd = Command()
        cmd.mtype = MTYPES[d[MKEYS.mtype.name]]
        if cmd.mtype == MTYPES.STATUS:
            raise RuntimeError("Kann Status-Message nicht parsen")
        if not cmd.mtype == MTYPES.STARTUP:
            cmd.selected_generator = d[MKEYS.selected_generator.name]
        if cmd.mtype == MTYPES.COL_UPDATE:
            cmd.colsec = COL_SECT[d[MKEYS.colsec.name]]
            cmd.color = RGB[d[MKEYS.color.name]]
            cmd.value = d[MKEYS.value.name]
        return cmd

    @staticmethod
    def select_generator(gname):
        c = Command()
        c.mtype = MTYPES.GENERATOR_SELECT
        c.selected_generator = gname
        return c

    @staticmethod
    def col_update(gname,colsec,rgbcol,value):
        c = Command()
        c.mtype = MTYPES.COL_UPDATE
        c.selected_generator = gname
        c.colsec = colsec.name
        c.color = rgbcol
        c.value = value
        return c

    @staticmethod
    def startup():
        c = Command()
        c.mtype = MTYPES.STARTUP
        return c

    def json(self):
        d = {
                MKEYS.mtype.name: self.mtype.name,
            }
        if self.selected_generator:
            d[MKEYS.selected_generator.name] = self.selected_generator
        if self.colsec:
            d[MKEYS.colsec.name] = self.colsec
        if self.color:
            d[MKEYS.color.name] = self.color.name
        if self.value:
            d[MKEYS.value.name] = self.value
        return json.dumps(d)

    def __str__(self):
        return f"Cmd({self.mtype.name}/{self.selected_generator})"

class MsgTest(unittest.TestCase):

    def testCommand(self):
        c = Command.parse_json('{ "mtype": "GENERATOR_SELECT", "selected_generator":"A"}')
        self.assertEqual(c.mtype, MTYPES.GENERATOR_SELECT)
        self.assertEqual(c.selected_generator,"A")
        j2 = Command.select_generator("X").json()
        c2 = Command.parse_json(j2)
        self.assertEqual(c2.selected_generator,"X")
        j3 = Command.col_update("X",COL_SECT.Vordergrund,RGB.rot,127).json()
        c3 = Command.parse_json(j3)
        self.assertEqual(c3.colsec,COL_SECT.Vordergrund)
        self.assertEqual(c3.value,127)
        self.assertEqual(c3.color,RGB.rot)

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
const MK_colsec = "colsec";
const MK_color = "color";
const MK_value = "value";
const MK_colors = "colors";""")
if __name__ == "__main__":
    unittest.main()
