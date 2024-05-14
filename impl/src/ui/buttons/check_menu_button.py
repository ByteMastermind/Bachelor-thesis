from .base_button import BaseButton


class CheckMenuButton(BaseButton):
    """
    A class implementing a button in a selection (options)
    """

    def set_checked(self, checked):
        """Set the button to a state checked or unchecked"""
        if checked:
            self.setStyleSheet("border: 4px solid red;")
            self.setStyleSheet("""
                QPushButton {
                    background-color: #41545d;
                    color: white;
                    padding: 11px 0px;
                    border-radius: 5px;
                    font-size: 16px;
                    border: 4px solid red;
                }
                QPushButton:hover {
                    background-color: #3cb371;
                }
            """)
        else:
            self.set_default_style()
