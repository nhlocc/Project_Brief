import logging
from logging.handlers import RotatingFileHandler


class Logger:
    _instance = None

    def __new__(cls, log_file="game.log", log_level=logging.INFO):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logger = cls._instance.set_up_logger(log_file, log_level)
        return cls._instance

    @staticmethod
    def set_up_logger(log_file: str, log_level: int, max_bytes: int = 100000, backup_count: int = 5):
        """
        Description:
            This static method configures and returns a logger with the specified log file and log level.
        Parameters:
            log_file(str): The name of the log file where log entries will be saved.
            log_level(int): The logging level (e.g., logging.INFO, logging.DEBUG) for the logger.
            max_bytes(int): The maximum size of a log file before it is rotated (in bytes).
                            (Default is 100000 bytes)
            backup_count(int): The number of backup log files to keep. Default is 5 backup files.
        Returns:
            logger(object): The configured logger instance.
        """
        logger = logging.getLogger()
        logger.setLevel(log_level)

        # Create the RotatingFileHandler for log rotation.
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)

        # Define the log format.
        log_format = '%(asctime)s [%(levelname)s] [in %(filename)s:%(lineno)d] [%(name)s] - %(message)s'
        formatter = logging.Formatter(log_format)
        file_handler.setFormatter(formatter)

        # Create the stream handler to display log messages on the console.
        console_handler = logging.StreamHandler()
        # Define a formatter for console output to show only the message
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger
