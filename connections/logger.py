""" Remote connection loggers

    Objects designed to monitor and report
    on remote connection statuses

"""

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
        Updates status with latest status and updates the updated
        var with True if connection status has changed
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



    def report_connection(self):
        pass
