import logging

from PyQt5.QtWidgets import QHBoxLayout

import constants

from ..buttons import CustomButton
from ..output_window import OutputWindow
from ..toast import InfoToast
from .base_screen import BaseScreen
from .input_screen import InputScreen


class ChangeIDMFUltralightScreen(BaseScreen):
    def __init__(self, command_builder, logger, stacked_widget, file_handler, parent=None):
        super().__init__(command_builder, logger, stacked_widget, file_handler, parent)

        self.card_id = ""

        # Init of toasts
        self.add_toast("id_loaded", InfoToast(text="Card ID loaded.", duration=1.5, parent=self.stacked_widget))
        self.add_toast("loading", InfoToast(text="Loading...", duration=constants.TOAST_DISAPPEAR_PERIOD, parent=self.stacked_widget))
        self.add_toast("writing", InfoToast(text="Writing...", duration=constants.TOAST_DISAPPEAR_PERIOD, parent=self.stacked_widget))
        self.add_toast("write_sent", InfoToast(text="Changing ID is done. Verify by loading. ", duration=1.5, parent=self.stacked_widget))

        # Settings options
        self.settings = constants.GEN1  # Default settings

    def add_screens_to_stacked_widget(self):
        # Init of screens
        self.change_id_mf_ultralight_input_screen = InputScreen(
            self.command_builder,
            self.logger,
            self.stacked_widget,
            self.file_handler,
            self,
            (14))

        # Adding them to the stacked widget
        self.stacked_widget.addWidget(self.change_id_mf_ultralight_input_screen)

    def setup_content(self):
        self.info_label = OutputWindow(self)
        self.hbox = QHBoxLayout()
        self.load_button = CustomButton("Load ID", self.load_id)
        self.edit_button = CustomButton("Edit ID", lambda: self.switch_to_screen(self.change_id_mf_ultralight_input_screen))
        self.change_id_button = CustomButton("Change ID", self.change_id)
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))

        self.hbox.addWidget(self.load_button)
        self.hbox.addWidget(self.edit_button)

        self.print_info()
        self.change_id_button.set_enabled(False)

        self.layout.addWidget(self.info_label)
        self.layout.addLayout(self.hbox)
        self.layout.addWidget(self.change_id_button)
        self.layout.addWidget(self.back_button)
        self.layout.setStretch(0, 1)

    def set_all_buttons_enabled(self, enabled):
        self.edit_button.set_enabled(enabled)
        self.back_button.set_enabled(enabled)

        if self.card_id != "":
            self.change_id_button.set_enabled(enabled)

    def load_id(self):
        self.show_toast("loading")
        self.run_command(constants.LOAD_MF_ID)

    def change_id(self):
        self.show_toast("loading")
        self.run_command(constants.CHANGE_MF_ULTRALIGHT_ID, self.card_id)

    def react(self, command_name):
        if command_name == constants.CHANGE_MF_ULTRALIGHT_ID:
            self.hide_toasts()
            self.show_toast("write_sent")
        elif command_name == constants.LOAD_MF_ID:
            self.hide_toasts()
            new_id = self.command_builder.get_output()
            if len(new_id) != 14:
                self.logger.log(f"Loaded ID {new_id} is unknown size.", level=logging.WARNING)
            self.set_card(new_id)
            self.save_card(new_id)
            self.show_toast("id_loaded")
            self.logger.log(f"Loaded ID {new_id}", level=logging.INFO)
        else:
            self.logger.log(f"{__name__} encountered unknown command_name.", level=logging.WARNING)

    def print_info(self):
        self.info_label.set_text("Add own ID to proceed.")

    def print_card(self):
        self.info_label.set_text(f"Card will be written with:\n\nID: {self.card_id}\n")

    def set_card(self, new_id):
        self.card_id = new_id
        self.print_card()
        self.change_id_button.set_enabled(True)

    def save_card(self, new_id):
        pass

    def set_settings(self, settings):
        self.settings = settings
        if self.card_id != "":
            self.print_card()
