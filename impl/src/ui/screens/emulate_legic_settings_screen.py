import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget

import constants

from ..buttons import CustomButton
from ..buttons.check_menu_button import CheckMenuButton
from ..description import Description
from .base_screen import BaseScreen


class EmulateLegicSettingsScreen(BaseScreen):
    def setup_content(self):
        self.description_label = Description("Select card type for ID emulation:")
        self.mim22 = CheckMenuButton("Legic Prime MIM22", self.mim22_enabled)
        self.mim256 = CheckMenuButton("Legic Prime MIM256", self.mim256_enabled)
        self.mim1024 = CheckMenuButton("Legic Prime MIM1024", self.mim1024_enabled)
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.mim256.set_checked(True)
        self.now_checked = self.mim256

        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.mim22)
        self.button_layout.addWidget(self.mim256)
        self.button_layout.addWidget(self.mim1024)

        self.scroll_area.setWidget(QWidget())
        self.scroll_area.widget().setLayout(self.button_layout)

        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignBottom)

    def mim22_enabled(self):
        tag_type = constants.MIM22
        self.now_checked.set_checked(False)
        self.now_checked = self.mim22
        self.mim22.set_checked(True)
        self.parent_screen.set_settings(tag_type)
        self.logger.log(f"Selected {tag_type} tag for emulation.", level=logging.INFO)

    def mim256_enabled(self):
        tag_type = constants.MIM256
        self.now_checked.set_checked(False)
        self.now_checked = self.mim256
        self.mim256.set_checked(True)
        self.parent_screen.set_settings(tag_type)
        self.logger.log(f"Selected {tag_type} tag for emulation.", level=logging.INFO)

    def mim1024_enabled(self):
        tag_type = constants.MIM1024
        self.now_checked.set_checked(False)
        self.now_checked = self.mim1024
        self.mim1024.set_checked(True)
        self.parent_screen.set_settings(tag_type)
        self.logger.log(f"Selected {tag_type} tag for emulation.", level=logging.INFO)
