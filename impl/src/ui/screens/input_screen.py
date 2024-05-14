from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLineEdit

from ..buttons import CustomButton
from ..toast import InfoToast, WarningToast
from .base_screen import BaseScreen


class InputScreen(BaseScreen):
    def __init__(self, command_builder, logger, stacked_widget, file_handler, parent, id_lengths):
        super().__init__(command_builder, logger, stacked_widget, file_handler, parent)
        self.id_lengths = id_lengths
        self.id = ""

        # Init of toasts
        self.add_toast("success", InfoToast(text="ID successfully set.", duration=1.5, parent=self.stacked_widget))
        self.add_toast("no_more_allowed", WarningToast(text="Cannot add more characters.", duration=0.5, parent=self.stacked_widget))

    def setup_content(self):
        self.input = QLineEdit()
        self.input.setStyleSheet("font-size: 20px; background-color: #222222")
        self.input.setAlignment(Qt.AlignCenter)

        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()

        # Creating the keyboard
        self.i0_button = CustomButton("0", lambda: self.add_input('0'))
        self.i1_button = CustomButton("1", lambda: self.add_input('1'))
        self.i2_button = CustomButton("2", lambda: self.add_input('2'))
        self.i3_button = CustomButton("3", lambda: self.add_input('3'))
        self.i4_button = CustomButton("4", lambda: self.add_input('4'))
        self.i5_button = CustomButton("5", lambda: self.add_input('5'))
        self.i6_button = CustomButton("6", lambda: self.add_input('6'))
        self.i7_button = CustomButton("7", lambda: self.add_input('7'))
        self.i8_button = CustomButton("8", lambda: self.add_input('8'))
        self.i9_button = CustomButton("9", lambda: self.add_input('9'))
        self.ia_button = CustomButton("A", lambda: self.add_input('A'))
        self.ib_button = CustomButton("B", lambda: self.add_input('B'))
        self.ic_button = CustomButton("C", lambda: self.add_input('C'))
        self.id_button = CustomButton("D", lambda: self.add_input('D'))
        self.ie_button = CustomButton("E", lambda: self.add_input('E'))
        self.if_button = CustomButton("F", lambda: self.add_input('F'))

        self.confirm_button = CustomButton("Confirm", self.confirm)
        self.confirm_button.set_enabled(False)
        self.clear_button = CustomButton("Clear", self.clear)
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))

        self.hbox1.addWidget(self.i0_button)
        self.hbox1.addWidget(self.i1_button)
        self.hbox1.addWidget(self.i2_button)
        self.hbox1.addWidget(self.i3_button)
        self.hbox1.addWidget(self.i4_button)
        self.hbox1.addWidget(self.i5_button)
        self.hbox1.addWidget(self.i6_button)
        self.hbox1.addWidget(self.i7_button)
        self.hbox2.addWidget(self.i8_button)
        self.hbox2.addWidget(self.i9_button)
        self.hbox2.addWidget(self.ia_button)
        self.hbox2.addWidget(self.ib_button)
        self.hbox2.addWidget(self.ic_button)
        self.hbox2.addWidget(self.id_button)
        self.hbox2.addWidget(self.ie_button)
        self.hbox2.addWidget(self.if_button)
        self.hbox3.addWidget(self.clear_button)
        self.hbox3.addWidget(self.confirm_button)

        self.layout.addWidget(self.input)
        self.layout.addLayout(self.hbox1)
        self.layout.addLayout(self.hbox2)
        self.layout.addLayout(self.hbox3)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignBottom)

    def confirm(self):
        self.id = self.input.text()
        self.parent_screen.save_card(self.id)
        self.parent_screen.set_card(self.id)
        self.show_toast("success")

    def add_input(self, input_char):
        if len(self.input.text()) == self.get_max_value(self.id_lengths):
            self.show_toast("no_more_allowed")
            return

        self.input.setText(self.input.text() + input_char)
        if len(self.input.text()) in self.make_iterable_if_not(self.id_lengths):
            self.confirm_button.set_enabled(True)
        else:
            self.confirm_button.set_enabled(False)

    def clear(self):
        self.input.setText("")
        self.confirm_button.set_enabled(False)

    def set_id_lengths(self, id_lengths):
        self.id_lengths = id_lengths

    @staticmethod
    def get_max_value(values):
        if isinstance(values, int):
            return values
        return max(values)

    @staticmethod
    def get_min_value(values):
        if isinstance(values, int):
            return values
        return min(values)

    @staticmethod
    def make_iterable_if_not(value):
        try:
            iter(value)
            return value  # If iterable, return as is
        except TypeError:
            return [value]  # If not iterable, wrap in a list and return
