""" Remote connection loggers

    Objects designed to monitor and report
    on remote connection statuses

"""

import os.path
import os
import datetime

class TeradiciLogger:
    """
    A logger class for monitoring and
    reporting Teradici connection statues

    ...

    Attributes
    ----------
    pc_name : str
        A string used for both identifying and connecting to
        PC you wish to monitor
    path_to_log : str
        Stores the default path to the teradici log files
    log_prefix : str
        Stores a string used to identify which log file to use
    user_name : str
        Stores the user that is reported to have connected via teradici
        this is filled by the function report_connection
    status : str
        Stores a string stating the current connections status
    updated : bool
        Stores a bool stating whether the connection status has been
        updated
    last_updated : list
        A list of two strings, [0] stating the date, [1] the time of last update
        this var is updated by the manager app


    Methods
    -------
    read_log_file() :
        Finds and reads log file and returns as list of strings
    check_for_update() :
        Checks if logs has been updated since last check
        returns with True if connection status has changed
    check_for_status() :
        Checks to see if there is a change of connection status
        amongst the new log messages
    create_update_message() :
        Creates human readable str with session variables



    """
    def __init__(self, pc_name, log_prefix='pcoip_agent_'):
        self.pc_name = pc_name
        self.path_to_log = f'//{pc_name}/c$/ProgramData/Teradici/PCoIPAgent/logs/'
        self.log_prefix = log_prefix
        self.user_name = ''
        self.status = ''
        self.updated = False
        self.last_updated = []

    def read_log_file(self):
        """ Finds and reads log file and returns as list of strings

        Raises
        ------
        FileNotFoundError
            If no log file or log path exists

        Returns
        -------
        log_contents : list
            A list of all lines in log file or error messages

        """

        log_contents = []

        # Find log file
        try:
            files_in_log_path = [f for f in os.listdir(self.path_to_log) if
                                 os.path.isfile(os.path.join(self.path_to_log, f))]

            try:
                # Uses prefix to identify correct log file
                for file in files_in_log_path:
                    if self.log_prefix in file:
                        log_file = file


                # Opens and returns contents of log file as a list
                with open(self.path_to_log + log_file, 'r') as log_file:
                    log_contents = list(log_file)
                return log_contents

            except FileNotFoundError:
                return 'Log file does not exist.'

        except FileNotFoundError:
            return f'No log folder found at {self.path_to_log}'


    def check_for_updates(self, log_file):
        """ Checks to see if log date is newer than previous and returns
        all lines with updated messages

        Parameters
        ----------
        log_file : list
            Requires list from read_log_file

        Raises
        ------
        TypeError:
            Returns type error if a string or int/float is inputted

        Returns
        -------
        new_log_messages : list
            List of updated lines only
        NoneType :
            If no updates found

        """

        new_log_messages = []

        try:

            for line in log_file:
                # Read date and time prefix and format it to compare
                # With last update time
                line_date = line[:19]
                line_date = line_date.split('T')

                # Test input is correct
                if len(line_date) <= 1 or len(line_date) > 2:
                    raise TypeError

                # Check if last update is greater than log date
                if line_date[0] >= self.last_updated[0]:
                    if line_date[1] > self.last_updated[1]:
                        new_log_messages.append(line)

            update_time = datetime.datetime.now()

            if len(new_log_messages) > 0:
                self.updated = True
                return new_log_messages
            else:
                self.updated = False
                return None

        except TypeError:
            return "Input is not a Teradici log list"

        except:
            return 'Unexpected error in logger.TeradiciLogger.check_for_updates()'



    def check_status(self, new_logs):
        """ Checks to see if there is a change of connection status
        amongst the new log messages

        Parameters
        ----------
        log_file : list
            Requires list from check_for_updates

        Raises
        ------
        TypeError:
            Returns type error if a string or int/float is inputted

        Returns
        -------
        current_session_var : list [ time_of_update : str, user_name : str, current_status : str ]
            Changes self.status and returns List of status info
        NoneType :
            Returns None if no status found amongst log messages

        """
        try:
            if type(new_logs) != list:
                raise TypeError

            # Reference Variables
            connection_messages = ["transition from CONNECTING --(CONNECTION_COMPLETE [102])--> CONNECTED", "transition from STOPPING -- STOPPING --(SERVER_STOPPED [202])--> INVALID"]
            user_name_message = "has activated, single sign on completed."
            status_found = False
            user_name_found = False
            new_logs =new_logs
            # Used as counter to iterate backwards through log messages
            line_num = len(new_logs)-1
            # Variables to extract from message
            latest_message = ''
            user_name = ""
            time_of_update = []
            current_status = ""
            # Return variable
            current_session_var = []

            # Finds the most recent line with a status message
            while True:
                if line_num < 0:
                    raise IndexError

                for message in connection_messages:
                    if message in new_logs[line_num]:
                        latest_message = new_logs[line_num]
                        status_found = True
                    else:
                        if user_name_message in new_logs[line_num] and not user_name_found:
                            # Process message to retrieve user name
                            user_name = new_logs[line_num]
                            user_name_found = True

                line_num -= 1

        except IndexError:
        # Ran out of lines to check

            # Check what data was found
            if status_found or user_name_found:

                if status_found:
                    # Process message to retrieve timestamp
                    time_of_update = latest_message[:19]
                    time_of_update = time_of_update.split('T')
                    # Process message to retrieve status
                    current_status = latest_message.split()
                    current_status = current_status[len(current_status)-1]
                    self.status = current_status

                if user_name_found:
                    user_name = user_name.split('user ')
                    user_name = user_name[1].split(' has activated')
                    user_name = user_name[0]
                    self.user_name = user_name
            else:
                # Didn't find any status messages
                return None


            current_session_var = time_of_update, user_name, current_status
            return current_session_var

        except TypeError:
            return "Input is not a Teradici log list"


    def create_update_message(self, session_variables):
        """ Creates human readable str with session variables

            Parameters
            ----------
            session_variables : list
                Requires list from check_status

            Raises
            ------
            TypeError:
                Returns type error if a string or int/float is inputted

            Returns
            -------
            update_message : str
                Human readable message for posting on slack and GUI

            """
        try:

            timestamp = " ".join(session_variables[0])
            connected_message_template = f"{timestamp} | {self.pc_name} is {session_variables[2]} | Active User : {session_variables[1]}"
            disconnected_message_template = f"{timestamp} | {self.pc_name} is DISCONNECTED | Last User : {self.user_name}"

            if type(session_variables) != list:
                raise TypeError

            if session_variables[2] == "CONNECTED":
                return connected_message_template
            elif session_variables[2] == "INVALID":
                return disconnected_message_template
            else:
                return "Error: Entered list does not appear to be a 'session_variable' list"


        except TypeError:
            return "Input is not a Teradici log list"



