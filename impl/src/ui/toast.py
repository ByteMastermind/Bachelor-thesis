from PyQt5.QtGui import QColor, QFont

from .toast_lib import Toast


class BaseToast(Toast):
    """
    A Base class that is describing how all the toast types should look

    Args:
        text (str): The text of the toast
        duration (float): How long the toast stays on the screen
        parent: The parent element
    """

    def __init__(self, text, duration, parent):
        super().__init__(text=text, duration=duration, parent=parent)
        self.set_background_color()
        self.setForegroundColor(QColor(30, 30, 30))
        self.setFont(QFont('Arial', 11))
        self.setOpacity(1.0)

    def set_background_color(self):
        """A pure virtual method, sets bachgrand color"""

        raise NotImplementedError(
            f"Subclasses must implement {__name__} method.")


class ErrorToast(BaseToast):
    """
    An error toast
    """

    def __init__(self, text, duration, parent):
        super().__init__(text=text, duration=duration, parent=parent)

    def set_background_color(self):
        self.setBackgroundColor(QColor(229, 65, 65))


class InfoToast(BaseToast):
    """
    An info toast
    """

    def __init__(self, text, duration, parent):
        super().__init__(text=text, duration=duration, parent=parent)

    def set_background_color(self):
        self.setBackgroundColor(QColor(117, 220, 220))


class WarningToast(BaseToast):
    """
    A warning toast
    """

    def __init__(self, text, duration, parent):
        super().__init__(text=text, duration=duration, parent=parent)

    def set_background_color(self):
        self.setBackgroundColor(QColor(239, 239, 141))
