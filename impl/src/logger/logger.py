import logging
import os

import constants


class Logger:
    """
    The Logger class takes care of the formating of the logs
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File Handler
        root_folder = os.path.expanduser(constants.ROOT_FOLDER)  # Expand tilde to full path
        file_handler = logging.FileHandler(os.path.join(root_folder, constants.LOG_FILE))
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log(self, message, level=logging.INFO):
        """
        Log a message with the specified log level.
        :param message: The message to log.
        :param level: The log level (default is INFO).
        """
        if level == logging.DEBUG:
            self.logger.debug(message)
        elif level == logging.INFO:
            self.logger.info(message)
        elif level == logging.WARNING:
            self.logger.warning(message)
        elif level == logging.ERROR:
            self.logger.error(message)
        elif level == logging.CRITICAL:
            self.logger.critical(message)
