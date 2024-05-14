import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget

import constants

from ..buttons import CheckMenuButton, CustomButton
from ..description import Description
from .base_screen import BaseScreen


class ChangeIDMFClassicSettingsScreen(BaseScreen):
    def setup_content(self):
        self.description_label = Description("Select MF Classic magic card capabilities:")
        self.gen1 = CheckMenuButton("GEN1 tag", self.gen1_enabled)
        self.gen3 = CheckMenuButton("GEN3 tag", self.gen3_enabled)
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.gen1.set_checked(True)
        self.now_checked = self.gen1

        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.gen1)
        self.button_layout.addWidget(self.gen3)

        self.scroll_area.setWidget(QWidget())
        self.scroll_area.widget().setLayout(self.button_layout)

        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignBottom)

    def gen1_enabled(self):
        encoding = constants.GEN1
        self.now_checked.set_checked(False)
        self.now_checked = self.gen1
        self.gen1.set_checked(True)
        self.parent_screen.set_settings(encoding)
        self.logger.log(f"Selected {encoding} encoding for writing.", level=logging.INFO)

    def gen3_enabled(self):
        encoding = constants.GEN3
        self.now_checked.set_checked(False)
        self.now_checked = self.gen3
        self.gen3.set_checked(True)
        self.parent_screen.set_settings(encoding)
        self.logger.log(f"Selected {encoding} encoding for writing.", level=logging.INFO)
