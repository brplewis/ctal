import unittest
from logger import TeradiciLogger

tal_logger = TeradiciLogger('wlringest10')

class TestTeradiciLoggerRead(unittest.TestCase):
    def test_read_log_file(self):
        # Tests output is a list
        self.assertIsInstance(tal_logger.read_log_file(), list)
        # Test output is all lines in file
        self.assertGreaterEqual(len(tal_logger.read_log_file()), 5)
