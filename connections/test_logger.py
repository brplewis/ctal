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
        tal_logger.last_updated = ["2020-05-19", "13:27:41"]
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


class TestTeradiciLoggerStatus(unittest.TestCase):
    def test_check_status(self):
        tal_logger = TeradiciLogger('wlringest10')
        test_list = ["2020-05-19T16:27:41.217Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :1444 WINDOWS SESSION EVENT: set session: 1, event: WTS_SESSION_LOCK.",
            "2020-05-19T16:27:41.217Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :1444 ====== WINDOWS SESSION INFO ======",
            "2020-05-19T16:27:41.219Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :1444 Session ID: 1, session name: Console, session user: EVOLUTIONS\ops.wlr, session type: WTS_PROTOCOL_TYPE_CONSOLE, state: WTSActive, WTSSESSION_CHANGE(0x7).",
            "2020-05-19T16:27:41.226Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :1444 SESSION CHANGE: session ID 1, message: WTS_SESSION_LOCK, server running: NO, rwc server running : NO",
            "2020-05-19T16:27:45.014Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :1554 Server has been gone for 21 seconds, restoring state."]
        # Test no status update
        self.assertIsNone(tal_logger.check_status(test_list))

        #Test Disconnected status
        test_list = ["2020-05-21T14:40:58.058Z f684cd80-7d9e-1038-a745-000000000000 > LVL:2 RC:   0           AGENT :1244 Connection COMPLETE: code=(0)",
            "2020-05-21T14:40:58.058Z f684cd80-7d9e-1038-a745-000000000000 > LVL:2 RC:   0           AGENT :1244 -------------------------------------------------------------------",
            "2020-05-21T14:40:58.059Z 00000000-0000-0000-0000-000000000000 > LVL:1 RC:   0           AGENT :-----------------------------------------------------------------------",
            "2020-05-20T19:21:53.699Z 00000000-0000-0000-0000-000000000000 > LVL:1 RC:   0           AGENT :transition from STOPPING -- STOPPING --(SERVER_STOPPED [202])--> INVALID",
            "2020-05-21T14:40:58.060Z 00000000-0000-0000-0000-000000000000 > LVL:1 RC:   0           AGENT :-----------------------------------------------------------------------"]
        self.assertEqual(tal_logger.check_status(test_list)[2], "INVALID")

        # Test Connection complete status
        test_list = ["2020-05-21T14:40:58.058Z f684cd80-7d9e-1038-a745-000000000000 > LVL:2 RC:   0           AGENT :1244 Connection COMPLETE: code=(0)",
            "2020-05-21T14:40:58.058Z f684cd80-7d9e-1038-a745-000000000000 > LVL:2 RC:   0           AGENT :1244 -------------------------------------------------------------------",
            "2020-05-21T14:40:58.059Z 00000000-0000-0000-0000-000000000000 > LVL:1 RC:   0           AGENT :-----------------------------------------------------------------------",
            "2020-05-21T14:40:58.059Z 00000000-0000-0000-0000-000000000000 > LVL:1 RC:   0           AGENT :transition from CONNECTING --(CONNECTION_COMPLETE [102])--> CONNECTED",
            "2020-05-21T14:40:58.060Z 00000000-0000-0000-0000-000000000000 > LVL:1 RC:   0           AGENT :-----------------------------------------------------------------------",
            "2020-05-21T14:40:58.060Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :cSERVER_SESSION::send_acknowledgement sending ack.",
            "2020-05-21T14:40:58.060Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :send_message, 8 bytes",
            "2020-05-21T14:40:58.160Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :cSERVER_SESSION::send_acknowledgement succeeded to srvr0005",
            "2020-05-21T14:42:29.302Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :cSERVER_SESSION::agent_receiver_callback: message from A:srvr5;B:srvr0005 to A:srvr5, message = 16 00 00 00, len=20"]
        self.assertEqual(tal_logger.check_status(test_list)[2], "CONNECTED" )
        # Test Time stamp
        self.assertEqual(tal_logger.check_status(test_list)[0], ["2020-05-21", "14:40:58"])

        # Test Disconnected status
        test_list = ["2020-05-21T14:40:55.433Z f684cd80-7d9e-1038-a745-000000000000 > LVL:2 RC:   0           AGENT :1754 SSO: user DOMAIN\John.Williams has activated, single sign on completed.",
            "2020-05-21T14:40:58.058Z f684cd80-7d9e-1038-a745-000000000000 > LVL:2 RC:   0           AGENT :1244 -------------------------------------------------------------------",
            "2020-05-21T14:40:58.059Z 00000000-0000-0000-0000-000000000000 > LVL:1 RC:   0           AGENT :-----------------------------------------------------------------------",
            "2020-05-20T19:21:53.699Z 00000000-0000-0000-0000-000000000000 > LVL:1 RC:   0           AGENT :transition from STOPPING -- STOPPING --(SERVER_STOPPED [202])--> INVALID",
            "2020-05-21T14:40:58.060Z 00000000-0000-0000-0000-000000000000 > LVL:1 RC:   0           AGENT :-----------------------------------------------------------------------",
            "2020-05-21T14:40:58.060Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :cSERVER_SESSION::send_acknowledgement sending ack.",
            "2020-05-21T14:40:58.060Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :send_message, 8 bytes",
            "2020-05-21T14:40:58.160Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :cSERVER_SESSION::send_acknowledgement succeeded to srvr0005",
            "2020-05-21T14:42:29.302Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :cSERVER_SESSION::agent_receiver_callback: message from A:srvr5;B:srvr0005 to A:srvr5, message = 16 00 00 00, len=20",
            ]
        self.assertEqual(tal_logger.check_status(test_list)[2], "INVALID")
        # test for User_name when after message
        self.assertEqual(tal_logger.check_status(test_list)[1], "DOMAIN\John.Williams")
        test_list = [
            "2020-05-21T14:40:55.433Z f684cd80-7d9e-1038-a745-000000000000 > LVL:2 RC:   0           AGENT :1754 SSO: user DOMAIN\John.Williams has activated, single sign on completed.",
            "2020-05-21T14:40:58.058Z f684cd80-7d9e-1038-a745-000000000000 > LVL:2 RC:   0           AGENT :1244 -------------------------------------------------------------------",
            "2020-05-21T14:40:58.059Z 00000000-0000-0000-0000-000000000000 > LVL:1 RC:   0           AGENT :-----------------------------------------------------------------------",
            "2020-05-20T19:21:53.699Z 00000000-0000-0000-0000-000000000000 > LVL:1 RC:   0           AGENT :transition from STOPPING -- STOPPING --(SERVER_STOPPED [202])--> INVALID",
            "2020-05-21T14:40:58.060Z 00000000-0000-0000-0000-000000000000 > LVL:1 RC:   0           AGENT :-----------------------------------------------------------------------",
            "2020-05-21T14:40:58.060Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :cSERVER_SESSION::send_acknowledgement sending ack.",
            "2020-05-21T14:40:58.060Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :send_message, 8 bytes",
            "2020-05-21T14:40:58.160Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :cSERVER_SESSION::send_acknowledgement succeeded to srvr0005",
            "2020-05-21T14:42:29.302Z 00000000-0000-0000-0000-000000000000 > LVL:2 RC:   0           AGENT :cSERVER_SESSION::agent_receiver_callback: message from A:srvr5;B:srvr0005 to A:srvr5, message = 16 00 00 00, len=20",
            "2020-05-21T14:40:55.433Z f684cd80-7d9e-1038-a745-000000000000 > LVL:2 RC:   0           AGENT :1754 SSO: user DOMAIN\John.Williams has activated, single sign on completed."]
        # Test TypeError Str
        self.assertEqual(tal_logger.check_status("Test list"), "Input is not a Teradici log list")
        # Test TypeError int
        self.assertEqual(tal_logger.check_status(2), "Input is not a Teradici log list")
        # Test TypeError float
        self.assertEqual(tal_logger.check_status(2.01), "Input is not a Teradici log list")
        # Test output is List
        self.assertIsInstance(tal_logger.check_status(test_list), list)

class TestTeradiciLoggerMessage(unittest.TestCase):
    def test_create_update_report(self):
        tal_logger = TeradiciLogger('wlringest10')
        # Test Connected message
        self.assertEqual(tal_logger.create_update_message([['2020-05-21', '14:40:58'], 'DOMAIN\John.Williams', 'CONNECTED']), '2020-05-21 14:40:58 | wlringest10 is CONNECTED | Active User : DOMAIN\John.Williams\n')
        # Test Disconnected message
        tal_logger.user_name = 'DOMAIN\John.Williams'
        self.assertEqual(tal_logger.create_update_message([['2020-05-21', '14:40:58'], '', 'INVALID']), '2020-05-21 14:40:58 | wlringest10 is DISCONNECTED | Last User : DOMAIN\John.Williams\n')
        # Check for wrong list error
        self.assertEqual(tal_logger.create_update_message(['Something', 20, 'Wrong']), "Error: Entered list does not appear to be a 'session_variable' list")
        # Test TypeError Str
        self.assertEqual(tal_logger.create_update_message("Test list"), "Input is not a Teradici log list")
        # Test TypeError int
        self.assertEqual(tal_logger.create_update_message(2), "Input is not a Teradici log list")
        # Test TypeError float
        self.assertEqual(tal_logger.create_update_message(2.01), "Input is not a Teradici log list")

