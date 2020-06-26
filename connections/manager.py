""" Logger Manager

    The main control app for Ctal. It manages
    and deploys loggers while also having functions
    to update the GUI and Slack channels

"""

# Program Modules
import connections.logger as logger

# Internal Modules
import os
import datetime

# External Modules
import mysql.connector


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
        logger_groups : list
            List of all logger group names
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
        create_logger_group() :
            Creates a new SQL table for monitoring group
        initial_status() :
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
        get_status_data() :
            Gets status data from database for updates
        update_slack() :
            Updates slack channel with text table
        create_summary_table() :
            Creates a text tables of the summary data



                """

    def __init__(self):
        self.all_loggers = []
        self.loggers = {}
        self.logger_groups = []
        self.database_ip = ''
        self.database = None
        self.slack_channel = ''
        self.slack_key = ''
        self.last_updated = []
        self.database = None
        self.database_name = ''
        self.database_version = ''

    def get_loggers(self):
        """ Sends a list of all monitored pcs / loggers and it's group

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
                current_logger = []
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

    def get_logger_and_group(self):
        logger_and_group = []
        for logger in self.loggers.keys():
            log = []
            log.append(logger)
            log.append(self.loggers[logger])
            logger_and_group.append(log)
        return logger_and_group


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
                    new_instance = logger.TeradiciLogger(pc_name, group=group)
                else:
                    new_instance = logger.TeradiciLogger(pc_name, label=label, group=group)
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
                status_log = logger_status
                # Check for error messages
                if status_log is str:
                    error_message = status_log
                    raise ValueError

                time = status_log[0][0] + ' ' + status_log[0][1]

                pc_name = logger_inst.pc_name
                final_log = []

                final_log.append(time)
                final_log.append(pc_name)
                final_log.append(status_log[2])
                final_log.append(status_log[1])



                last_updated = str(datetime.datetime.now()).split()
                self.last_updated = last_updated
                logger_inst.last_updated = last_updated
                return final_log

            else:
                raise TypeError

        except TypeError:
            return "Input is not a TeradiciLogger or RDP logger"

        except ValueError:
            self.process_error(error_message)

        except Exception as error:
            return f"Unsuccessful | Error message : {error}"

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
                log_updates = logger_inst.check_status(log_updates)
                summary_log.append(log_updates)

            return summary_log

        except ValueError:
            self.process_error(error_message)
            return error_message



    """def get_update(self, group="all"):"""
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

    """try:
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
        return error_message"""

    def connect_to_database(self, host="127.0.0.1", database="ctal", user="root", password=".cred"):
        """ Connects to mysql database and applies objects and variables to
            self.database variables

            Parameters
            ----------
            host : str [optional]
                Requires a IP address or hostname for MYSql server
            database : str [optional]
                Requires the name of the database
            user : str [optional]
                Requires username of user with full permissions
            password : str [optional]
                Requires the filename of a file that contains your password

            Raises
            ------
            Exception:
                This is a catch all that returns the error message as a part of
                a connection message
            Returns
            -------
            str:
                Returns a connection message as a string

        """

        try:
            home = os.getenv("HOME")
            password = f"{home}/{password}"
            # Retrieve password and removes \n
            with open(password, 'r') as file:
                password = file.readline()
                password = password[:len(password) - 1]

            # Connect to database
            connection = mysql.connector.connect(host=host,
                                                 database=database,
                                                 user=user,
                                                 password=password,
                                                 autocommit=True)

            cursor = connection.cursor()
            # cursor.execute("select database();")

            # Assign variables

            self.database = connection
            self.database_version = connection.get_server_info()
            self.database_name = database

            return "Successful | Connection status: Connected"

        except Exception as error:
            return f"Unsuccessful | Error message : {error}"

    def load_config(self):
        """ Loads config settings

            Raises
            ------
            TypeError:
                When input is not a config file
            ValueError:
                When config contents does not match config format

            Returns
            -------
            str:
                Returns status message

        """
        pass

    def save_config(self):
        """ Loads config settings

            Raises
            ------
            TypeError:
                When input is not a config file
            ValueError:
                When config contents does not match config format

            Returns
            -------
            str:
                Returns status message

        """
        pass

    def create_logger_group(self, group_name):
        """ Add new logger group to self.logger_groups and
            creates a new table in the database

            Raises
            -----

            ValueError:
                When group name is already used

            Returns
            -------
            str:
                Returns status message

        """
        try:
            if group_name in self.logger_groups:
                raise ValueError

            # Add new group name to list
            self.logger_groups.append(group_name)

            # Create table
            database_cursor = self.database.cursor()
            database_cursor.execute(f"CREATE TABLE {group_name} ("
                                    f"time VARCHAR(50), pc_name VARCHAR(50), status VARCHAR(50), user VARCHAR(50), pc_ID int PRIMARY KEY AUTO_INCREMENT);")

            return f"{group_name} group was successfully created."

        except ValueError:
            return "ERROR: Group already exists"

        except Exception as error:
            return f"Unsuccessful | Error message : {error}"


    def get_groups(self):
        """ Get list of group names


            Raises
            -----

            IndexError:
                When update_list is not the correct format

            Returns
            -------
            str:
                Returns status message

        """

        table_list = []

        database_cursor = self.database.cursor(buffered=True)
        database_cursor.execute(f"SHOW TABLES;")

        for status in database_cursor:
            table_list.append(status[0])

        return table_list


    def update_database(self, group_name, update_list):
        """ Add pc status data to group tables.


            Parameters
            ----------
            group_name : str
                Requires a group name for table SQL table selection
            update_list : list
                Requires a list of status variable from get_update()

            Raises
            -----

            IndexError:
                When update_list is not the correct format

            Returns
            -------
            str:
                Returns status message

        """
        try:
            database_cursor = self.database.cursor(buffered=True)

            #for update in update_list:
            time = update_list[0]
            pc_name = update_list[1]
            status = update_list[2]
            user = update_list[3]

            # check if pc_name is in group
            database_cursor.execute(f"SELECT status FROM {group_name} WHERE {group_name}.pc_name = '{pc_name}';")
            if database_cursor.fetchone() is None:
                database_cursor.execute(f"INSERT INTO {group_name} (time, pc_name, status, user) VALUES ('{time}', '{pc_name}', '{status}', '{user}');")
            else:
                database_cursor.execute(f"UPDATE WLR SET time = '{time}', status = '{status}', user = '{user}' WHERE pc_name = '{pc_name}';")

            return "Update Complete"

        except IndexError:
            return "ERROR: Update_list error, bad formatting"

    def get_status_data(self, group_name):
        """ Add pc status data to group tables.

            Parameters
            ----------
            group_name : str
                Requires a group name for table SQL table selection
            update_list : list
                Requires a list of tuples containing pc name and status

            Raises
            -----

            IndexError:
                When update_list is not the correct format

            Returns
            -------
            str:
                Returns status message

        """

        summary_list = []

        database_cursor = self.database.cursor(buffered=True)
        database_cursor.execute(f"SELECT * FROM {group_name} ORDER BY length(pc_name), pc_name;")

        for status in database_cursor:
            summary_list.append(status)

        return summary_list

    def create_summary_table(self, summary_list, table_type):
        """ Takes summary list and converts it into a text tables
            for posting to slack and web GUI

            Parameters
            ----------
            summary_list : list
                Requires a summary list of statuses

            Raises
            -----
            TypeError:
                When update_list is not a list

            Returns
            -------
            str:
                Returns status message as text table

        """
        #try:

        if type(summary_list) is list:

            now = datetime.datetime.now()
            now = now.strftime("%Y-%m-%d %H:%M")

            if table_type == "slack":
                # Add slack formatting marks

                summary_log_full = [f"*=========== Update {now} ===========*\n"]

                for entry in summary_list:
                    summary_log_full.append(entry)
            else:
                # No slack formatting marks
                summary_log_full = [f"============ Update {now} ============\n"]

                for i in range(len(summary_list)):
                    #summary_log_full.append(summary_list[i])
                    if i == 0:
                        highest = i
                    elif i + 1 > len(summary_list):
                        break
                    elif summary_list[i][:4] > summary_list[i][:4]:
                        highest = i
                    elif summary_list[i][:4] < summary_list[i][:4]:
                        highest = i + 1

                summary_list[highest] = summary_list[highest][:len(summary_list[highest])-1]
                summary_list[highest] = f"<b> {summary_list[highest]} </b>\n"

                for i in summary_list:
                    summary_log_full.append(i)



            string_summary_table = "".join(summary_log_full)

            return string_summary_table
            #else:
                #raise TypeError


        #except TypeError:
            #return "ERROR: Input is not a summary list"
