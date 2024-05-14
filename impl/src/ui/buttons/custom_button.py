from .base_button import BaseButton


class CustomButton(BaseButton):
    """General normal button"""

    def __init__(self, text, command=None, parent=None):
        super().__init__(text=text, parent=parent, command=command)
