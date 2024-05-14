import logging

from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QWidget

from ..toast import ErrorToast
from ..worker import Worker


class BaseScreen(QWidget):
    """
    A base class of all the screens

    It provides basic methods how the screen should behave and exchange variables.
    Also there is implemented the toast logic and threading.

    Args:
        command_builder (CommandBuilder): The command builder
        logger (Logger): The logger
        stacked_widget (stackedWidget): The Q stacked widget used for screen switching
        file_handler (FileHandler): The file handler
        parent: The parent element
    """

    def __init__(self, command_builder, logger, stacked_widget, file_handler, parent=None):
        super().__init__(parent)
        self.parent_screen = parent
        self.file_handler = file_handler
        self.stacked_widget = stacked_widget
        self.command_builder = command_builder
        self.logger = logger
        self.__thread = QtCore.QThread()
        self.toasts_dict = {}
        self.layout = QVBoxLayout(self)
        self.add_screens_to_stacked_widget()
        self.setup_content()

    def run_command(self, command_name, supplement=None):
        """Runs specific command in a thread if another thread is not already running"""

        if not self.__thread.isRunning():
            self.set_all_buttons_enabled(False)
            self.__thread = self.__get_thread(command_name, supplement)
            self.__thread.start()

    def stop_command(self):
        """Force stops a thread"""

        if self.__thread.isRunning():
            self.__thread.quit()

    def __get_thread(self, command_name, supplement=None):
        """Returns a thread"""

        thread = QtCore.QThread()
        worker = Worker(self.command_builder, command_name, supplement)
        worker.moveToThread(thread)

        thread.worker = worker

        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)

        worker.reaction.connect(lambda value: self._react(value, command_name))

        return thread

    def add_screens_to_stacked_widget(self):
        """A virtual method that is handling adding the screens to a stacked widget"""

    def setup_content(self):
        """A pure virtual method where the class should specify the content of the widget"""

        raise NotImplementedError(f"Subclasses must implement {__name__} method.")

    def _react(self, reaction, command_name):
        """A part of reaction handling which is similiar to all derived classes"""

        self.logger.log(f"Received reaction {reaction} to command {command_name}.", level=logging.INFO)
        self.set_all_buttons_enabled(True)
        if reaction == "output_handled":
            self.react(command_name)
            return
        text = ""
        if reaction == "missing_reader":
            text = "Missing the reader"
        elif reaction == "missing_pm3":
            text = "The pm3 program is missing."
        elif reaction == "No card found":
            text = "No card found"
        elif reaction == "unknown_output":
            text = "Encountered unknown output."
        elif reaction == "problem":
            text = "Encountered a problem, try again."
        elif reaction == "nothing":
            text = "nothing"
        if reaction != "":
            self.hide_toasts()
            self.stop_command()
            self.logger.log(text, level=logging.WARNING)
            self.add_toast("reaction", ErrorToast(text=text, duration=1.5, parent=self.stacked_widget))
            self.show_toast("reaction")
        self.additional_react(text, command_name)

    def additional_react(self, text, command_name):
        """A virtul method where derived classes can implement its addition react to a command output"""

    def react(self, command_name):
        """The actual reaction of the derived class is described here"""

    def set_all_buttons_enabled(self, enabled):
        """A virtual method where all derived classes define the buttons that should be enabled or denabled"""

    def get_name(self):
        """Returns the class name"""
        return self.__class__.__name__

    def hide_toasts(self):
        """Hides all toasts associated with the screen"""
        for toast in self.toasts_dict.values():
            toast.hide()

    def show_toast(self, toast_name):
        """Shows the specified toast"""
        if toast_name in self.toasts_dict:
            self.toasts_dict[toast_name].show()
            self.toasts_dict[toast_name].raise_()
        else:
            self.logger.log(f"Toast named {toast_name} does not exist.", level=logging.WARNING)

    def add_toast(self, toast_name, toast):
        """Creates a new toast so it is later ready to use"""
        self.toasts_dict[toast_name] = toast

    def switch_to_screen(self, screen):
        """A method which handles the switching of the screens"""
        self.hide_toasts()
        self.log_screen_switch(screen.get_name())
        self.stacked_widget.setCurrentWidget(screen)

    def log_screen_switch(self, screen_name):
        """A method that logs the event of a screen switch"""
        self.logger.log(f"Switching to {screen_name} screen.", level=logging.INFO)
