import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget

import constants

from ..buttons import CustomButton
from ..buttons.check_menu_button import CheckMenuButton
from ..description import Description
from .base_screen import BaseScreen


class EmulateMFUltralightSettingsScreen(BaseScreen):
    def setup_content(self):
        self.description_label = Description("Select card type for emulation:")
        self.mfu = CheckMenuButton("Mifare Ultralight tag", self.mfu_enabled)
        self.mfu_ev1 = CheckMenuButton("Mifare Ultralight EV1 tag", self.mfu_ev1_enabled)
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.mfu.set_checked(True)
        self.now_checked = self.mfu

        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.mfu)
        self.button_layout.addWidget(self.mfu_ev1)

        self.scroll_area.setWidget(QWidget())
        self.scroll_area.widget().setLayout(self.button_layout)

        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignBottom)

    def mfu_enabled(self):
        tag_type = constants.MFU
        self.now_checked.set_checked(False)
        self.now_checked = self.mfu
        self.mfu.set_checked(True)
        self.parent_screen.set_settings(tag_type)
        self.logger.log(f"Selected {tag_type} tag for emulation.", level=logging.INFO)

    def mfu_ev1_enabled(self):
        tag_type = constants.MFU_EV1
        self.now_checked.set_checked(False)
        self.now_checked = self.mfu_ev1
        self.mfu_ev1.set_checked(True)
        self.parent_screen.set_settings(tag_type)
        self.logger.log(f"Selected {tag_type} tag for emulation.", level=logging.INFO)
