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
    def __init__(self, pc_name, log_path=f'//{self.pc_name}/c$/ProgramData/Teradici/PCoIPAgent/logs/', log_prefix='pcoip_agent_'):
        self.pc_name = pc_name
        self.path_to_log = log_path
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
            If no log file exists
        Returns
        -------

        """



        log_contents = []

        with open(f'{self.path_to_log}{self.}', 'r') as log_file:
            for line in log_file:
                log_contents.append(line)


    def check_for_update(self):
        """Checks if logs has been updated since last check
        returns with True if connection status has changed

        Parameters
        ----------


        Raises
        ------
        FileNotFoundError
            If no log file exists
        """

        log_file = ''

        # Find log file using prefix
        try:
            files_in_log_path = [f for f in os.listdir(self.path_to_log) if os.path.isfile(os.path.join(self.path_to_log, f))]

            try:
                for file in files_in_log_path:
                    if self.log_prefix in file:
                        log_file = file
            except FileNotFoundError:
                print('Log file does not exist.')

        except FileNotFoundError:
            print(f'No log folder found at {self.path_to_log}')



        with open(f'{}{}', 'r') as log_file:
            for lines in


        pass


