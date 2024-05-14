from PyQt5.QtCore import Qt

from ..buttons import CustomButton
from .base_screen import BaseScreen
from .change_id_mf_classic_screen import ChangeIDMFClassicScreen
from .change_id_mf_ultralight_screen import ChangeIDMFUltralightScreen


class ChangeIDMenuScreen(BaseScreen):
    def add_screens_to_stacked_widget(self):
        # Init of screens
        self.change_id_mf_classic_screen = ChangeIDMFClassicScreen(self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)
        self.change_id_mf_ultralight_screen = ChangeIDMFUltralightScreen(
            self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)

        # Adding them to the stacked widget
        self.stacked_widget.addWidget(self.change_id_mf_classic_screen)
        self.stacked_widget.addWidget(self.change_id_mf_ultralight_screen)

    def setup_content(self):
        self.mf_classic_button = CustomButton("Change MF Classic ID", lambda: self.switch_to_screen(self.change_id_mf_classic_screen))
        self.mf_ultralight_button = CustomButton("Change MF Ultralight ID", lambda: self.switch_to_screen(self.change_id_mf_ultralight_screen))

        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))

        self.layout.addWidget(self.mf_classic_button)
        self.layout.addWidget(self.mf_ultralight_button)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignBottom)
