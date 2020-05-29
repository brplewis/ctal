""" Logger Manager

    The main control app for Ctal. It manages
    and deploys loggers while also having functions
    to update the GUI and Slack channels


"""

import logger
import os
import datetime


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
        add_logger() :
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

            # Gets name of each logger object
            for logger in self.all_loggers:
                if logger.pc_name == logger.label:
                    list_loggers.append(logger.pc_name)
                else:
                    list_loggers.append(logger.label)

            return list_loggers

        except IndexError:
            # No loggers in list
            return "No loggers have been initialize"
        except:
            # Issue with fetching name or logger var
            return "Unexpected error: Please check you have set up your loggers correctly"


    def add_logger(self, pc_name, logger_type, label=None, group=None):
        """ Creates a new logger instance and adds it to the
            the all_loggers and loggers{}

            Raises
            ------
            TypeError:
                When input is not a str
            ValueError:
                When input hostname does not exist

            Returns
            -------
                Returns "Complete" string

            """

        try:
            if type(pc_name) != str:
                raise TypeError

            if not os.path.isdir(f'/mnt/{pc_name}/ProgramData'):
                raise ValueError

            if logger_type == 'teradici':
                # Adds label if needed
                if label is None:
                    new_instance = logger.TeradiciLogger(pc_name)
                else:
                    new_instance = logger.TeradiciLogger(pc_name, label=label)
                # Logger number for connecting dictionary entry
                # to logger objects in list
                logger_number = len(self.all_loggers)
                self.all_loggers.append(new_instance)
                # Use label over pc_name if one is used
                if label is None:
                    self.loggers[pc_name] = (group, logger_number)
                else:
                    self.loggers[label] = (group, logger_number)

                # Run initial status check
                self.initial_status(new_instance)
                return 'Complete'


        except ValueError:
            return f"{pc_name} does not exist."

        except TypeError:
            return "Enter the PC name or IP as a string"

        except:
            return "Unexpected Error: Please check your input values"



    def initial_status(self, logger_inst):
        """ Gets status of new logger

            Raises
            ------
            TypeError:
                When logger_inst is not a TeradiciLogger or RDPLogger object

            Returns
            -------
            update_summary : list
                Returns a list of update summaries

        """
        try:
            # Variable fir error reporting
            error_message = ''

            if isinstance(logger_inst, logger.TeradiciLogger) or isinstance(logger_inst, logger.RDPLogger):

                log_contents = logger_inst.read_log_file()
                # Check for error messages
                if log_contents is str:
                    error_message = log_contents
                    raise ValueError
                logger_status = logger_inst.check_status(log_contents)
                # Check for error messages
                if logger_status is str:
                    error_message = logger_status
                    raise ValueError
                status_log = logger_inst.create_update_message(logger_status)
                # Check for error messages
                if status_log is str:
                    error_message = status_log
                    raise ValueError

                last_updated = str(datetime.datetime.now()).split()
                self.last_updated = last_updated
                logger_inst.last_updated = last_updated
                return status_log

            else:
                raise TypeError

        except TypeError:
            return "Input is not a TeradiciLogger or RDP logger"

        except ValueError:
            self.process_error(error_message)

        except:
            return "Unexpect Error: Please check your logger instance"


    def process_error(self, error_message):
        print(error_message)


    def get_update(self, group="all"):
        """ Gets update summaries from all or a group of
            loggers

            Raises
            ------
            TypeError:
                When input is not a str
            ValueError:
                When input hostname does not exist

            Returns
            -------
            update_summary : list
                Returns a list of update summaries

        """

        try:
            group = group
            summary_log = []
            logger_list = []

            if group == 'all':
                logger_list = self.all_loggers

            else:
                for logger_inst in self.loggers:
                    if self.loggers[logger_inst][0] == group:
                        logger_position = self.loggers[logger_inst][1]
                        logger_list.append(self.all_loggers[logger_position])

            # Fetch summaries
            for logger_inst in logger_list:
                log_contents = logger_inst.read_log_file()
                # Check for error messages
                if log_contents is str:
                    error_message = log_contents
                    raise ValueError
                log_updates = logger_inst.check_for_updates(log_contents)
                # Check for error messages
                if log_updates is str:
                    error_message = log_contents
                    raise ValueError
                logger_status = logger_inst.check_status(log_updates)
                # Check for error messages
                if logger_status is str:
                    error_message = log_contents
                    raise ValueError

                summary_log.append(logger_inst.create_update_message(logger_status))
            return summary_log




        except ValueError:
            self.process_error(error_message)
            return error_message











