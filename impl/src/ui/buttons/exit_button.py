from .base_button import BaseButton


class ExitButton(BaseButton):
    """Class describing the design of the exit button"""

    def set_default_style(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #ff6347;
                color: white;
                padding: 11px 0px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ffa347;
            }
        """)
