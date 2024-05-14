from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel


class OutputWindow(QLabel):
    """
    A window that shows text on a dark background

    Used for displaying the output or some information

    Args:
        parent: The parent element
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #222222;padding: 7px; font-size: 16px;")
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setWordWrap(True)

    def set_text(self, text):
        self.setText(text)
