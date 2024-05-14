from PyQt5.QtCore import Qt

from ..buttons import CustomButton
from .base_screen import BaseScreen
from .clone_em410x_menu_screen import CloneEM410XMenuScreen
from .clone_legic_menu_screen import CloneLegicMenuScreen
from .clone_mf_classic_menu_screen import CloneMFClassicMenuScreen
from .clone_mf_ultralight_menu_screen import CloneMFUltralightMenuScreen


class CloneMenuScreen(BaseScreen):
    def add_screens_to_stacked_widget(self):
        # Init of screens
        self.clone_em410x_menu_screen = CloneEM410XMenuScreen(self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)
        self.clone_legic_menu_screen = CloneLegicMenuScreen(self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)
        self.clone_mf_classic_menu_screen = CloneMFClassicMenuScreen(self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)
        self.clone_mf_ultralight_menu_screen = CloneMFUltralightMenuScreen(
            self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)

        # Adding them to the stacked widget
        self.stacked_widget.addWidget(self.clone_em410x_menu_screen)
        self.stacked_widget.addWidget(self.clone_legic_menu_screen)
        self.stacked_widget.addWidget(self.clone_mf_classic_menu_screen)
        self.stacked_widget.addWidget(self.clone_mf_ultralight_menu_screen)

    def setup_content(self):
        self.ex410_button = CustomButton("Clone EM410x card", lambda: self.switch_to_screen(self.clone_em410x_menu_screen))
        self.legic_button = CustomButton("Clone Legic Prime card", lambda: self.switch_to_screen(self.clone_legic_menu_screen))
        self.mf_classic_button = CustomButton("Clone MF Classic card", lambda: self.switch_to_screen(self.clone_mf_classic_menu_screen))
        self.mf_ultralight_button = CustomButton("Clone MF Ultralight card", lambda: self.switch_to_screen(self.clone_mf_ultralight_menu_screen))
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))

        self.layout.addWidget(self.ex410_button)
        self.layout.addWidget(self.legic_button)
        self.layout.addWidget(self.mf_classic_button)
        self.layout.addWidget(self.mf_ultralight_button)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignBottom)
