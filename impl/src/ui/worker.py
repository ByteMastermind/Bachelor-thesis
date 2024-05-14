from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal


class Worker(QtCore.QObject):
    """
    A Worker is a class describing the threading operations and its outputs

    The operations are the commands send to the proxmark.
    Otherwise without usage of this threading technique the screen would freeze for the amount of time when the
    command is executed by the proxmark.

    Args:
        command_builder (CommandBuilder): The command builder
        command_name (str): The command name
        supplement (str): Additional arguments to the command
    """
    reaction = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, command_builder, command_name, supplement=None):
        super().__init__()
        self.command_builder = command_builder
        self.command_name = command_name
        self.supplement = supplement

    def run(self):
        reaction = "nothing"    # Default reaction
        reaction = self.command_builder.command(self.command_name, self.supplement)
        self.reaction.emit(reaction)
        self.finished.emit()
