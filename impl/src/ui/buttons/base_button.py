from PyQt5.QtWidgets import QPushButton


class BaseButton(QPushButton):
    """
    A base class describing the designg of the button

    Also implementing methods.

    Args:
        text (str): The text in the button
        command: The function to be executed on click
        parent: The parent element
    """

    def __init__(self, text, command=None, parent=None):
        super().__init__(text, parent)
        if command:
            self.clicked.connect(command)
        self.set_default_style()

    def set_enabled(self, enabled):
        """Sets the button enabled - visuals and makes it not clickable"""

        self.setEnabled(enabled)
        self.setStyleSheet(
            self.styleSheet() +
            "QPushButton:disabled { color: rgba(0, 0, 0, 0.5); }")

    def set_default_style(self):
        """Setting the default style"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #41545d;
                color: white;
                padding: 11px 0px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #3cb371;
            }
        """)
