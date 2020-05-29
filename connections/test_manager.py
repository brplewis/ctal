import unittest
from manager import Manager
from logger import TeradiciLogger

manager_init = Manager()

class TestManager(unittest.TestCase):
    def test_add_logger(self):
        # test for successful creation
        self.assertEqual(manager_init.add_logger('wlringest14', 'teradici'), "Complete")
        # Test non existent pc
        self.assertEqual(manager_init.add_logger('wlringest24', 'teradici'), "wlringest24 does not exist.")
        # Test error from input type
        self.assertEqual(manager_init.add_logger(20, 'teradici'), "Enter the PC name or IP as a string")
        # Test dictionary creation
        self.assertEqual(manager_init.loggers, {'wlringest14': (None, 0)})
        self.assertEqual(manager_init.add_logger('wlringest8', 'teradici', label="WLRINGEST8", group='WLR'), "Complete")
        self.assertEqual(manager_init.loggers, {'WLRINGEST8': ('WLR', 1), 'wlringest14': (None, 0)})

    def test_get_loggers(self):
        # Check it returns correct output
        self.assertEqual(manager_init.get_loggers(), ["wlringest14", "WLRINGEST8"])

    def test_initial_status(self):
        # Check correct summary format
        self.assertIsInstance(manager_init.initial_status(manager_init.all_loggers[0]), str)
        # Check input error catching
        self.assertEqual(manager_init.initial_status("Test"), "Input is not a TeradiciLogger or RDP logger")


    def test_get_update(self):
        #Check output
        manager_init.add_logger('wlringest4', 'teradici', label="WLRINGEST5")
        self.assertEqual(len(manager_init.get_update()), 3)
        # Test group output
        self.assertEqual(len(manager_init.get_update('WLR')), 1)
        print(manager_init.get_update('WLR'))

