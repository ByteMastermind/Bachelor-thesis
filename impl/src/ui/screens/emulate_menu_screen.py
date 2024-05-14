from PyQt5.QtCore import Qt

from ..buttons import CustomButton
from .base_screen import BaseScreen
from .emulate_id_menu_screen import EmulateIDMenuScreen
from .emulate_legic_menu_screen import EmulateLegicMenuScreen
from .emulate_mf_classic_menu_screen import EmulateMFClassicMenuScreen
from .emulate_mf_ultralight_menu_screen import EmulateMFUltralightMenuScreen


class EmulateMenuScreen(BaseScreen):
    def add_screens_to_stacked_widget(self):
        # Init of screens
        self.emulate_id_menu_screen = EmulateIDMenuScreen(self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)
        self.emulate_legic_menu_screen = EmulateLegicMenuScreen(self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)
        self.emulate_mf_classic_menu_screen = EmulateMFClassicMenuScreen(
            self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)
        self.emulate_mf_ultralight_menu_screen = EmulateMFUltralightMenuScreen(
            self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)

        # Adding them to the stacked widget
        self.stacked_widget.addWidget(self.emulate_id_menu_screen)
        self.stacked_widget.addWidget(self.emulate_legic_menu_screen)
        self.stacked_widget.addWidget(self.emulate_mf_classic_menu_screen)
        self.stacked_widget.addWidget(self.emulate_mf_ultralight_menu_screen)

    def setup_content(self):
        self.id_button = CustomButton("Emulate ID", lambda: self.switch_to_screen(self.emulate_id_menu_screen))
        self.legic_button = CustomButton("Emulate Legic Prime card", lambda: self.switch_to_screen(self.emulate_legic_menu_screen))
        self.mf_classic_button = CustomButton("Emulate MF Classic card", lambda: self.switch_to_screen(self.emulate_mf_classic_menu_screen))
        self.mf_ultralight_button = CustomButton("Emulate MF Ultralight card", lambda: self.switch_to_screen(self.emulate_mf_ultralight_menu_screen))

        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))

        self.layout.addWidget(self.id_button)
        self.layout.addWidget(self.legic_button)
        self.layout.addWidget(self.mf_classic_button)
        self.layout.addWidget(self.mf_ultralight_button)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignBottom)
