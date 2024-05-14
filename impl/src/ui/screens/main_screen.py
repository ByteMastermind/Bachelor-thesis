import logging

import constants

from ..buttons import CustomButton, ExitButton
from .base_screen import BaseScreen
from .change_id_menu_screen import ChangeIDMenuScreen
from .clone_menu_screen import CloneMenuScreen
from .emulate_menu_screen import EmulateMenuScreen
from .search_output_screen import SearchOutputScreen


class MainScreen(BaseScreen):
    def add_screens_to_stacked_widget(self):
        # Init of screens
        self.search_output_screen = SearchOutputScreen(self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)
        self.clone_menu_screen = CloneMenuScreen(self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)
        self.emulate_menu_screen = EmulateMenuScreen(self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)
        self.change_id_menu_screen = ChangeIDMenuScreen(self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)

        # Adding them to the stacked widget
        self.stacked_widget.addWidget(self.search_output_screen)
        self.stacked_widget.addWidget(self.clone_menu_screen)
        self.stacked_widget.addWidget(self.emulate_menu_screen)
        self.stacked_widget.addWidget(self.change_id_menu_screen)

    def setup_content(self):
        self.low_freq_search_button = CustomButton("Low frequency search", lambda: self.to_search_screen(constants.LF_SEARCH))
        self.high_freq_search_button = CustomButton("High frequency search", lambda: self.to_search_screen(constants.HF_SEARCH))
        self.clone_button = CustomButton("Clone card", lambda: self.switch_to_screen(self.clone_menu_screen))
        self.emulate_button = CustomButton("Emulate card", lambda: self.switch_to_screen(self.emulate_menu_screen))
        self.change_id_button = CustomButton("Change ID", lambda: self.switch_to_screen(self.change_id_menu_screen))
        self.exit_button = ExitButton("Exit", self.parent().exit)

        self.layout.addWidget(self.low_freq_search_button)
        self.layout.addWidget(self.high_freq_search_button)
        self.layout.addWidget(self.clone_button)
        self.layout.addWidget(self.emulate_button)
        self.layout.addWidget(self.change_id_button)
        self.layout.addWidget(self.exit_button)

    def to_search_screen(self, command_name):
        self.switch_to_screen(self.search_output_screen)
        method_to_call = getattr(self.search_output_screen, command_name, None)
        if method_to_call:
            method_to_call()
        else:
            self.logger.log(f"Method {command_name} not found.", level=logging.WARNING)
