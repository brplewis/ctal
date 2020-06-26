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
        # Check output
        manager_init.add_logger('wlringest4', 'teradici', label="WLRINGEST5")
        self.assertEqual(len(manager_init.get_update()), 3)
        print(manager_init.get_update())
        # Test group output
        self.assertEqual(len(manager_init.get_update('WLR')), 1)
        print(manager_init.get_update('WLR'))

    def test_connect_to_database(self):
        # Test successful connection
        self.assertEqual(manager_init.connect_to_database(host='10.10.30.77', user='bob'),
                         "Successful | Connection status: Connected")
        # Test unsuccessful connection
        self.assertEqual(manager_init.connect_to_database(host='10.10.30.77', user='john'),
                         "Unsuccessful | Error message : 1045 (28000): Access denied for user 'john'@'10.10.30.252' ("
                         "using password: YES)")

    def test_create_group(self):
        self.assertEqual(manager_init.connect_to_database(host='10.10.30.77', user='bob'),
                         "Successful | Connection status: Connected")
        # Test creation of group in list
        self.assertEqual(manager_init.create_logger_group('WLR'), "WLR group was successfully created.")

    def test_add_to_database(self):
        self.assertEqual(manager_init.connect_to_database(host='10.10.30.77', user='bob'),
                         "Successful | Connection status: Connected")
        # Test creation of group in list
        # self.assertEqual(manager_init.create_logger_group('WLR'), "WLR group was successfully created.")
        # Test successful data addition
        summary_list = [["wlringest14", "12:00 | wlringest14 is CONNECTED | Active User : ops.wlr"],
                        ["wlringest11", "10:00 | wlringest11 is CONNECTED | Active User : ops.wlr"],
                        ["wlringest8", "16:00 | wlringest8 is CONNECTED | Active User : ops.wlr"]]
        self.assertEqual(manager_init.update_database("WLR", summary_list), "Update Complete")

    def test_get_status_data(self):
        pass

    def test_create_summary_table(self):
        print(type(["11:00 Status 1\n", "11:12 status 2\n", "18:01 status 3\n"]))
        summary_list = ["2020-05-21 14:40:58 | wlringest14 is CONNECTED | Active User : ops.wlr\n",
                        "2020-06-11 14:40:58  is CONNECTED | Active User : ops.wlr\n",
                        "2020-05-21 15:10:58  is CONNECTED | Active User : ops.wlr\n"]
        print(manager_init.create_summary_table(summary_list, "gui"))
        # self.assertEqual(manager_init.create_summary_table(["Status 1", "status 2", "status 3"]) )
