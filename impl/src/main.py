import logging
import os
import sys

from PyQt5.QtWidgets import QApplication

import constants
from commands import CommandBuilder, CommandExecutor, OutputHandler
from file_handler import FileHandler
from logger import Logger
from ui import MainWindow

# Replace 'path_to_src_folder' with the actual path to your src folder
sys.path.append('./src')


if __name__ == "__main__":
    # Check if the directory exists
    root_folder = os.path.expanduser(constants.ROOT_FOLDER)  # Expand tilde to full path
    if not os.path.exists(root_folder):
        print(constants.ROOT_FOLDER)
        print("Program directoty does not exist. Run install.sh script first.")
        sys.exit(-1)

    logger = Logger()
    logger.log("Starting cloner program.", level=logging.INFO)
    file_handler = FileHandler(logger)
    output_handler = OutputHandler(logger)
    command_executor = CommandExecutor(output_handler, logger)
    command_builder = CommandBuilder(command_executor, logger)

    app = QApplication(sys.argv)
    window = MainWindow(command_builder, logger, file_handler)
    window.show()
    sys.exit(app.exec())
