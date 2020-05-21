import unittest
from logger import TeradiciLogger



class TestTeradiciLoggerRead(unittest.TestCase):
    def test_read_log_file(self):
        tal_logger = TeradiciLogger('wlringest10')
        # Tests output is a list
        self.assertIsInstance(tal_logger.read_log_file(), list)
        # Test output is all lines in file
        self.assertGreaterEqual(len(tal_logger.read_log_file()), 5)



class TestTeradiciLoggerCheck(unittest.TestCase):
    def test_check_for_updates(self):
        tal_logger = TeradiciLogger('wlringest10')
        tal_logger.last_updated = ["2020-05-19", "13:27:41"]
        test_list = ["2020-05-19T16:27:41.217Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :1444 WINDOWS SESSION EVENT: set session: 1, event: WTS_SESSION_LOCK.",
                    "2020-05-19T16:27:41.217Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :1444 ====== WINDOWS SESSION INFO ======",
                    "2020-05-19T16:27:41.219Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :1444 Session ID: 1, session name: Console, session user: EVOLUTIONS\ops.wlr, session type: WTS_PROTOCOL_TYPE_CONSOLE, state: WTSActive, WTSSESSION_CHANGE(0x7).",
                    "2020-05-19T16:27:41.226Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :1444 SESSION CHANGE: session ID 1, message: WTS_SESSION_LOCK, server running: NO, rwc server running : NO",
                    "2020-05-19T16:27:45.014Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :1554 Server has been gone for 21 seconds, restoring state."]
        # Test to see if output is a  list
        self.assertIsInstance(tal_logger.check_for_updates(test_list), list)
        # Test to see if it detects updates
        self.assertGreater(len(tal_logger.check_for_updates(test_list)), 0)
        # Test to see if it ignores old lines
        tal_logger.last_updated = ["2020-05-19", "20:27:41"]
        self.assertIsNone(tal_logger.check_for_updates(test_list))
        # Test error handling for string
        self.assertEqual(tal_logger.check_for_updates('String input'), "Input is not a Teradici log list")
        # Test error handling int
        self.assertEqual(tal_logger.check_for_updates(10), "Input is not a Teradici log list")
        # Test Error handling for float
        self.assertEqual(tal_logger.check_for_updates(1.002), "Input is not a Teradici log list")
        # Test Error handling for incorrect list short
        self.assertEqual(tal_logger.check_for_updates(["Log message 1", "Log Message 2"]), "Input is not a Teradici log list")
        # Test Error handling for incorrect list short
        self.assertEqual(tal_logger.check_for_updates(["Log message 1 xxxxxxxxxxxxxxxxxxxxxxxxx ", "Log Message 2 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx "]),
                         "Input is not a Teradici log list")
