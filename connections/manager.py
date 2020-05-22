""" Logger Manager

    The main control app for Ctal. It manages
    and deploys loggers while also having functions
    to update the GUI and Slack channels


"""

class Manager:
    """
        Main suite of functions for controlling
        and deploying loggers

        ...

        Attributes
        ----------
        all_loggers : list
            List of logger objects
        loggers : Dict
            A dictionary of loggers and their database table
        database_ip : str
            IP address and port info for connecting to
            SQL database
        database : object
            Database object for communicating with SQL
        slack_channel : str
            Slack_channel info
        slack_key : str
            A path to slack key
        last_updated : list
            Holds the timestamp of last update. Date and time
            as separate strings

        Methods
        -------

        get_loggers() :
            Returns a list of strings stating the names
            of all active loggers
        get_monitoring_groups() :
            Returns all the monitoring groups (eg. WLR, SPR)
        connect_to_database() :
            Connects to SQL database and retrieves config
        load_config() :
            Loads config file from database
        launch_new_logger() :
            Sets up a new logger instance
        create_logger_table() :
            Creates a new SQL table for monitoring group
        first_check() :
            Like check_for_updates but it grabs the latest change
            regardless of last_updated
        check_for_updates() :
            Checks all loggers for updates and returns a list
            of session_summaries
        create_text_update_table() :
            Combines all session summaries into a text table
            for slack and database log
        update_database() :
            Update the database with session summaries and log
        update_slack() :
            Updates slack channel with text table



                """
    def __init__(self):
        self.all_loggers = []
        self.loggers = {}
        self.database_ip = ''
        self.database = None
        self.slack_channel = ''
        self.slack_key = ''
        self.last_updated = []

    def get_loggers(self):
        """ Sends a list of all monitored pcs / loggers

        Raises
        ------
        IndexError:
            When no loggers have been set up

        Returns
        -------
            List of the names of all loggers

        """

        try:
            # Check Loggers have been loaded into list
            if len(self.all_loggers) == 0:
                raise IndexError

            list_loggers = []

            for logger in all_loggers:
                list_loggers.append(logger.pc_name)

            return list_loggers

        except IndexError:
            # No loggers in list
            return "No loggers have been initialize"
        except:
            # Issue with fetching name or logger var
            return "Unexpected error: Please check you have set up your loggers correctly"


    def launch_new_logger(self, pc_name, type):
        pass

