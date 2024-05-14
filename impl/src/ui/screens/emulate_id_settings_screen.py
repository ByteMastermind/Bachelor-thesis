import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget

import constants

from ..buttons import CustomButton
from ..buttons.check_menu_button import CheckMenuButton
from ..description import Description
from .base_screen import BaseScreen


class EmulateIDSettingsScreen(BaseScreen):
    def __init__(self, command_builder, logger, stacked_widget, file_handler, parent, input_screen):
        super().__init__(command_builder, logger, stacked_widget, file_handler, parent)
        self.input_screen = input_screen

    def setup_content(self):
        self.description_label = Description("Select card type for ID emulation:")
        self.em410x = CheckMenuButton("EM410X tag", self.em410x_enabled)
        self.mf_classic_1k = CheckMenuButton("MF Classic 1k tag", self.mf_classic_1k_enabled)
        self.mf_classic_4k = CheckMenuButton("MF Classic 4k tag", self.mf_classic_4k_enabled)
        self.mf_desfire = CheckMenuButton("MF Desfire tag", self.mf_desfire_enabled)
        self.mf_ultralight = CheckMenuButton("MF Ultralight tag", self.mf_ultralight_enabled)
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.em410x.set_checked(True)
        self.now_checked = self.em410x

        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.em410x)
        self.button_layout.addWidget(self.mf_classic_1k)
        self.button_layout.addWidget(self.mf_classic_4k)
        self.button_layout.addWidget(self.mf_desfire)
        self.button_layout.addWidget(self.mf_ultralight)

        self.scroll_area.setWidget(QWidget())
        self.scroll_area.widget().setLayout(self.button_layout)

        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignBottom)

    def em410x_enabled(self):
        tag_type = constants.EM410X
        self.now_checked.set_checked(False)
        self.now_checked = self.em410x
        self.em410x.set_checked(True)
        self.input_screen.set_id_lengths(10)
        self.parent_screen.set_settings(tag_type)
        self.logger.log(f"Selected {tag_type} tag for emulation.", level=logging.INFO)

    def mf_classic_1k_enabled(self):
        tag_type = constants.MF_CLASSIC_1K
        self.now_checked.set_checked(False)
        self.now_checked = self.mf_classic_1k
        self.mf_classic_1k.set_checked(True)
        self.input_screen.set_id_lengths((8, 10, 14))
        self.parent_screen.set_settings(tag_type)
        self.logger.log(f"Selected {tag_type} tag for emulation.", level=logging.INFO)

    def mf_classic_4k_enabled(self):
        tag_type = constants.MF_CLASSIC_4K
        self.now_checked.set_checked(False)
        self.now_checked = self.mf_classic_4k
        self.mf_classic_4k.set_checked(True)
        self.input_screen.set_id_lengths((8, 10, 14))
        self.parent_screen.set_settings(tag_type)
        self.logger.log(f"Selected {tag_type} tag for emulation.", level=logging.INFO)

    def mf_desfire_enabled(self):
        tag_type = constants.MF_DESFIRE
        self.now_checked.set_checked(False)
        self.now_checked = self.mf_desfire
        self.mf_desfire.set_checked(True)
        self.input_screen.set_id_lengths((8, 14))
        self.parent_screen.set_settings(tag_type)
        self.logger.log(f"Selected {tag_type} tag for emulation.", level=logging.INFO)

    def mf_ultralight_enabled(self):
        tag_type = constants.MF_ULTRALIGHT
        self.now_checked.set_checked(False)
        self.now_checked = self.mf_ultralight
        self.mf_ultralight.set_checked(True)
        self.input_screen.set_id_lengths((8, 10, 14))
        self.parent_screen.set_settings(tag_type)
        self.logger.log(f"Selected {tag_type} tag for emulation.", level=logging.INFO)
