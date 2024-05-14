
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea

import constants

from ..buttons import CustomButton
from ..output_window import OutputWindow
from ..toast import InfoToast
from .base_screen import BaseScreen


class SearchOutputScreen(BaseScreen):
    def __init__(self, command_builder, logger, stacked_widget, file_handler, parent=None):
        super().__init__(command_builder, logger, stacked_widget, file_handler, parent)
        self.output = ""

        # Init of toasts
        self.add_toast("loading", InfoToast(text="Loading...", duration=120, parent=self.stacked_widget))

    def setup_content(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.text_output = OutputWindow(self)

        self.scroll_area.setWidget(self.text_output)
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))

        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignBottom)

    def set_all_buttons_enabled(self, enabled):
        self.back_button.set_enabled(enabled)

    def lf_search(self):
        self.set_output("Low frequency search is running.")
        self.show_toast("loading")
        self.run_command(constants.LF_SEARCH)

    def hf_search(self):
        self.set_output("High frequency search is running.")
        self.show_toast("loading")
        self.run_command(constants.HF_SEARCH)

    def react(self, command_name):
        self.hide_toasts()
        self.set_output(self.command_builder.get_output())

    def additional_react(self, text, command_name):
        self.set_output(text)

    def set_output(self, output):
        self.text_output.setText(output)
