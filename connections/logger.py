""" Remote connection loggers

    Objects designed to monitor and report
    on remote connection statuses

"""

import os.path
import os

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


    Methods
    -------

    check_for_update()
        Checks if logs has been updated since last check
        returns with True if connection status has changed
    report_connection()
        Returns the connection status and info as a list to be used
        for database entry


    """
    def __init__(self, pc_name, log_prefix='pcoip_agent_'):
        self.pc_name = pc_name
        self.path_to_log = f'//{pc_name}/c$/ProgramData/Teradici/PCoIPAgent/logs/'
        self.log_prefix = log_prefix
        self.username = ''
        self.status = ''
        self.updated = False
        self.last_updated = ''

    def read_log_file(self):
        """ Finds and reads log file and returns as list of strings

        Raises
        ------
        FileNotFoundError
            If no log file or log path exists

        Returns
        -------
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
        List of updated lines only or None

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









