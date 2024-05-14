import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget

import constants

from ..buttons import CheckMenuButton, CustomButton
from ..description import Description
from .base_screen import BaseScreen


class CloneEM410XSettingsScreen(BaseScreen):
    def setup_content(self):
        self.description_label = Description("Select encoding for writing (default T55X7):")
        self.t55x7 = CheckMenuButton("T55X7 tags", self.t55x7_enabled)
        self.q5 = CheckMenuButton("Q5/T5555 tags", self.q5_enabled)
        self.em4305 = CheckMenuButton("EM4305/4460 tags", self.em4305_enabled)
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.t55x7.set_checked(True)
        self.now_checked = self.t55x7

        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.t55x7)
        self.button_layout.addWidget(self.q5)
        self.button_layout.addWidget(self.em4305)

        self.scroll_area.setWidget(QWidget())
        self.scroll_area.widget().setLayout(self.button_layout)

        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignBottom)

    def t55x7_enabled(self):
        encoding = constants.T55X7
        self.now_checked.set_checked(False)
        self.now_checked = self.t55x7
        self.t55x7.set_checked(True)
        self.parent_screen.set_settings(encoding)
        self.logger.log(f"Selected {encoding} encoding for writing.", level=logging.INFO)

    def q5_enabled(self):
        encoding = constants.Q5
        self.now_checked.set_checked(False)
        self.now_checked = self.q5
        self.q5.set_checked(True)
        self.parent_screen.set_settings(encoding)
        self.logger.log(f"Selected {encoding} encoding for writing.", level=logging.INFO)

    def em4305_enabled(self):
        encoding = constants.EM4305
        self.now_checked.set_checked(False)
        self.now_checked = self.em4305
        self.em4305.set_checked(True)
        self.parent_screen.set_settings(encoding)
        self.logger.log(f"Selected {encoding} encoding for writing.", level=logging.INFO)
