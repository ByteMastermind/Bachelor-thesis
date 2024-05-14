from PyQt5.QtWidgets import QLabel


class Description(QLabel):
    """
    Defines how the description labels should look

    Args:
        text (str): The text in the label
        parent: The parent element
    """

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.set_default_style()

    def set_default_style(self):
        self.setStyleSheet("""
            QLabel {
                qproperty-indent:0;
                color: white;
                padding-top: 0px;
                padding-bottom: 0px;
                font-size: 18px;
                margin: 0px;
                           }
        """)
