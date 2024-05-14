import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget

import constants

from ..buttons import CustomButton
from ..buttons.check_menu_button import CheckMenuButton
from ..description import Description
from .base_screen import BaseScreen


class EmulateMFClassicSettingsScreen(BaseScreen):
    def setup_content(self):
        self.description_label = Description("Select card type for ID emulation:")
        self.mf_classic_1k = CheckMenuButton("MF Classic 1k tag", self.mf_classic_1k_enabled)
        self.mf_classic_2k = CheckMenuButton("MF Classic 2k tag", self.mf_classic_2k_enabled)
        self.mf_classic_4k = CheckMenuButton("MF Classic 4k tag", self.mf_classic_4k_enabled)
        self.mf_classic_mini = CheckMenuButton("MF Classic mini tag", self.mf_classic_mini_enabled)
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.mf_classic_1k.set_checked(True)
        self.now_checked = self.mf_classic_1k

        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.mf_classic_1k)
        self.button_layout.addWidget(self.mf_classic_2k)
        self.button_layout.addWidget(self.mf_classic_4k)
        self.button_layout.addWidget(self.mf_classic_mini)

        self.scroll_area.setWidget(QWidget())
        self.scroll_area.widget().setLayout(self.button_layout)

        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignBottom)

    def mf_classic_1k_enabled(self):
        tag_type = constants.MF_CLASSIC_1K
        self.now_checked.set_checked(False)
        self.now_checked = self.mf_classic_1k
        self.mf_classic_1k.set_checked(True)
        self.parent_screen.set_settings(tag_type)
        self.logger.log(f"Selected {tag_type} tag for emulation.", level=logging.INFO)

    def mf_classic_2k_enabled(self):
        tag_type = constants.MF_CLASSIC_2K
        self.now_checked.set_checked(False)
        self.now_checked = self.mf_classic_2k
        self.mf_classic_2k.set_checked(True)
        self.parent_screen.set_settings(tag_type)
        self.logger.log(f"Selected {tag_type} tag for emulation.", level=logging.INFO)

    def mf_classic_4k_enabled(self):
        tag_type = constants.MF_CLASSIC_4K
        self.now_checked.set_checked(False)
        self.now_checked = self.mf_classic_4k
        self.mf_classic_4k.set_checked(True)
        self.parent_screen.set_settings(tag_type)
        self.logger.log(f"Selected {tag_type} tag for emulation.", level=logging.INFO)

    def mf_classic_mini_enabled(self):
        tag_type = constants.MF_CLASSIC_MINI
        self.now_checked.set_checked(False)
        self.now_checked = self.mf_classic_mini
        self.mf_classic_mini.set_checked(True)
        self.parent_screen.set_settings(tag_type)
        self.logger.log(f"Selected {tag_type} tag for emulation.", level=logging.INFO)
