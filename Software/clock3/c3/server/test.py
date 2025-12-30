import asyncio, json
from .controler import Controler
from .messages import MKEYS, MTYPES, Command
from .genset import ConStatus, TestGenSet

import unittest

class MockSpi:
    def __init__(self):
        self.received = []
    def putbytes(self,bs):
        self.received.append(bs)

class MockReceiver:
    def __init__(self,con):
        self.con = con
        self.msgs = []
        self.status_counter = 0
        self.selected_generators = []

    async def receive(self):
        try:
            async for message in self.con.subscribe():
                d = json.loads(message)
                if d[MKEYS.mtype.name] == MTYPES.STATUS.name:
                    self.status_counter += 1
                    self.selected_generators.append( d[MKEYS.selected_generator.name] )
                self.msgs.append(d)
        except asyncio.CancelledError:
            pass

class ControlerTest(unittest.TestCase):

    async def startStop(self,con):
        t = asyncio.create_task(con.run())
        await asyncio.sleep(7)
        t.cancel()
        await t

    def testStartStop(self):
        spi = MockSpi()
        con = Controler(TestGenSet(),spi)
        asyncio.run(self.startStop(con))
        self.assertEqual(len(spi.received),2)
        self.assertEqual(len(spi.received[0]),3*3)

    async def switch(self,con,recv):
        t = asyncio.create_task(con.run())
        r = asyncio.create_task(recv.receive())
        await asyncio.sleep(2)
        await con.handle_command(Command.select_generator("C"))
        await asyncio.sleep(0.01)
        await con.handle_command(Command.select_generator("B"))
        await asyncio.sleep(6)
        await con.handle_command(Command.startup())
        await asyncio.sleep(6)
        t.cancel()
        await t
        r.cancel()
        await r

    def testSwitch(self):
        spi = MockSpi()
        con = Controler(TestGenSet(),spi)
        recv = MockReceiver(con)
        asyncio.run(self.switch(con,recv))
        self.assertEqual(len(spi.received),5)
        self.assertEqual(len(spi.received[0]),3*3)
        self.assertEqual(len(spi.received[1]),3*3)
        self.assertEqual(len(recv.msgs),4)
        self.assertEqual(recv.status_counter,4)
        self.assertEqual(recv.selected_generators,"A C B B".split())

    def testMsg(self):
        c = ConStatus()
        ks = c.msg_dict().keys()
        self.assertIn(MKEYS.generators.name, ks)
        self.assertIn(MKEYS.selected_generator.name, ks)
        self.assertGreater( len(json.dumps(c.msg_dict())),50)
        #self.assertEqual(json.dumps(c.msg_dict()),"")
