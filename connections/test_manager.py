import unittest
from manager import Manager
from logger import TeradiciLogger

manager_init = Manager()

class TestManager(unittest.TestCase):
    def test_get_loggers(self):
        logger1 = TeradiciLogger('wlringest14')
        logger2 = TeradiciLogger('wlringest14')
        # Check it returns correct output
        self.assertEqual(manager_init.get_loggers(), ["wlringest10", "wlringest14"])
