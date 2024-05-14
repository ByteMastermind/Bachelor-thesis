import configparser
import logging
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStackedWidget, QVBoxLayout, QWidget

import constants

from .screens import MainScreen


class MainWindow(QWidget):
    """
    The MainWindow is creating the window where the screens are displayed

    It also loads screen specs in the config file

    Args:
        command_builder (CommandBuilder): The command builder
        logger (Logger): The logger
        file_handler (FileHandler): The file handler
    """

    def __init__(self, command_builder, logger, file_handler):
        super().__init__()
        self.logger = logger
        self.command_builder = command_builder
        self.file_handler = file_handler
        self.stacked_widget = QStackedWidget(self)

        # Setting defaults for the config and getting info from the config
        self.enable_fullscreen = False
        self.screen_width = 480
        self.screen_height = 320
        self.enable_shutdown = False
        self.get_config()

        self.init_ui()

    def init_ui(self):
        """Init of the user interface"""
        self.layout = QVBoxLayout(self)

        # Setting the window size and style
        self.setFixedSize(self.screen_width, self.screen_height)
        if self.enable_fullscreen:
            self.showFullScreen()
        self.setWindowFlag(Qt.FramelessWindowHint)  # Frameless window enabled
        self.setStyleSheet("""
            background-color: #303030;
            color: white;
            font-family: Arial, sans-serif;
        """)

        # Initialize screen
        self.main_screen = MainScreen(self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)

        # Add screen to the stacked widget
        self.stacked_widget.addWidget(self.main_screen)

        # Add stacked widget to layout
        self.layout.addWidget(self.stacked_widget)

        # Show the main screen
        self.show_main_screen()

    def show_main_screen(self):
        self.main_screen.log_screen_switch(self.main_screen.get_name())
        self.stacked_widget.setCurrentWidget(self.main_screen)

    def exit(self):
        """Exiting the program

        It will close the program (and shut down the system) based on the config
        """
        self.logger.log("Program was closed.", level=logging.INFO)
        self.close()
        if not self.enable_shutdown:
            return

        # Execute the shutdown command
        self.logger.log("Shutting down the system.", level=logging.INFO)
        os.system("sudo shutdown -h now")

    def get_config(self):
        """Gets config from config file"""
        # Expand tilde to full path
        root_folder = os.path.expanduser(constants.ROOT_FOLDER)
        config_file_path = os.path.join(root_folder, constants.CONFIG_FILE)
        if not os.path.exists(config_file_path):
            self.logger.log(
                f"No {config_file_path} file found, taking defaults.",
                level=logging.WARNING)
            return  # Taking defaults

        # Create a ConfigParser object
        config = configparser.ConfigParser()

        # Read the config file
        # Assuming your config file is named config.ini
        config.read(config_file_path)

        # Get values from the config file
        try:
            self.enable_fullscreen = config.getboolean(
                'SCREEN', 'enable_fullscreen')
            self.screen_width = config.getint('SCREEN', 'screen_width')
            self.screen_height = config.getint('SCREEN', 'screen_height')
            self.enable_shutdown = config.getboolean(
                'DEFAULT', 'enable_shutdown')
        except Exception as e:
            self.logger.log(
                f"Error encountered while loading config file: {e}",
                level=logging.WARNING)

        # Log what has loaded
        self.logger.log(
            f"enable_fullscreen set to {self.enable_fullscreen}",
            level=logging.INFO)
        self.logger.log(
            f"screen_width set to {self.screen_width}",
            level=logging.INFO)
        self.logger.log(
            f"screen_height set to {self.screen_height}",
            level=logging.INFO)

        self.logger.log("Loading config done.", level=logging.INFO)
