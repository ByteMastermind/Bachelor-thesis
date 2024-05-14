import logging

from PyQt5.QtWidgets import QHBoxLayout

import constants

from ..buttons import CustomButton
from ..output_window import OutputWindow
from ..toast import InfoToast
from .base_screen import BaseScreen
from .clone_em410x_select_screen import CloneEM410XSelectScreen
from .clone_em410x_settings_screen import CloneEM410XSettingsScreen
from .input_screen import InputScreen


class CloneEM410XMenuScreen(BaseScreen):
    def __init__(self, command_builder, logger, stacked_widget, file_handler, parent=None):
        super().__init__(command_builder, logger, stacked_widget, file_handler, parent)

        self.card_id = ""

        # Init of toasts
        self.add_toast("id_loaded", InfoToast(text="Card ID loaded.", duration=1.5, parent=self.stacked_widget))
        self.add_toast("loading", InfoToast(text="Loading...", duration=constants.TOAST_DISAPPEAR_PERIOD, parent=self.stacked_widget))
        self.add_toast("writing", InfoToast(text="Writing...", duration=constants.TOAST_DISAPPEAR_PERIOD, parent=self.stacked_widget))
        self.add_toast("write_sent", InfoToast(text="Write signal has been sent. Verify by loading.", duration=1.5, parent=self.stacked_widget))

        # Settings options
        self.settings = constants.T55X7  # Default settings

    def add_screens_to_stacked_widget(self):
        # Init of screens
        self.clone_em410x_settings_screen = CloneEM410XSettingsScreen(self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)
        self.clone_em410x_select_screen = CloneEM410XSelectScreen(self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)
        self.clone_em410x_input_screen = InputScreen(self.command_builder, self.logger, self.stacked_widget, self.file_handler, self, id_lengths=10)

        # Adding them to the stacked widget
        self.stacked_widget.addWidget(self.clone_em410x_input_screen)
        self.stacked_widget.addWidget(self.clone_em410x_select_screen)
        self.stacked_widget.addWidget(self.clone_em410x_settings_screen)

    def setup_content(self):
        self.info_label = OutputWindow(self)
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.load_card_button = CustomButton("Load card", self.load_em410x_card)
        self.add_own_id_button = CustomButton("Add own ID", lambda: self.switch_to_screen(self.clone_em410x_input_screen))
        self.select_saved_card_button = CustomButton("Select saved card", self.to_select_screen)
        self.write_to_card_button = CustomButton("Write to card", self.write_to_card)
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))
        self.settings_button = CustomButton("⚙️ Settings", lambda: self.switch_to_screen(self.clone_em410x_settings_screen))

        self.print_info()
        self.write_to_card_button.set_enabled(False)

        self.hbox1.addWidget(self.load_card_button)
        self.hbox1.addWidget(self.add_own_id_button)
        self.hbox2.addWidget(self.select_saved_card_button)
        self.hbox2.addWidget(self.write_to_card_button)
        self.hbox3.addWidget(self.back_button)
        self.hbox3.addWidget(self.settings_button)

        self.layout.addWidget(self.info_label)
        self.layout.addLayout(self.hbox1)
        self.layout.addLayout(self.hbox2)
        self.layout.addLayout(self.hbox3)

        self.layout.setStretch(0, 1)

    def set_all_buttons_enabled(self, enabled):
        self.load_card_button.set_enabled(enabled)
        self.add_own_id_button.set_enabled(enabled)
        self.select_saved_card_button.set_enabled(enabled)
        self.back_button.set_enabled(enabled)
        self.settings_button.set_enabled(enabled)

        if self.card_id != "":
            self.write_to_card_button.set_enabled(enabled)

    def load_em410x_card(self):
        self.show_toast("loading")
        self.run_command(constants.LOAD_EM410X_ID)

    def write_to_card(self):
        self.show_toast("writing")
        if self.settings == constants.T55X7:
            self.run_command(constants.WRITE_EM410X_CARD, self.card_id)
        elif self.settings == constants.Q5:
            self.run_command(constants.WRITE_EM410X_CARD, self.card_id + " --q5")
        elif self.settings == constants.EM4305:
            self.run_command(constants.WRITE_EM410X_CARD, self.card_id + " --em")
        else:
            self.logger.log("Writing to em410x card encountered unknown settings.", level=logging.WARNING)

    def to_select_screen(self):
        self.clone_em410x_select_screen.refresh()
        self.switch_to_screen(self.clone_em410x_select_screen)

    def react(self, command_name):
        if command_name == constants.LOAD_EM410X_ID:
            self.hide_toasts()
            new_id = self.command_builder.get_output()
            if len(new_id) != 10:
                self.logger.log(f"Loaded ID {new_id} is not 10 characters.", level=logging.WARNING)
            self.set_card(new_id)
            self.save_card(new_id)
            self.show_toast("id_loaded")
            self.logger.log(f"Loaded ID {new_id}", level=logging.INFO)
        elif command_name == constants.WRITE_EM410X_CARD:
            self.hide_toasts()
            self.show_toast("write_sent")
        else:
            self.logger.log(f"{__name__} encountered unknown command_name.", level=logging.WARNING)

    def print_info(self):
        self.info_label.set_text("Cached card info:\nLoad card or add own ID to proceed.")

    def print_card(self):
        self.info_label.set_text(f"Card info:\nID: {self.card_id}\nWrite encoding settings: {self.settings}")

    def save_card(self, new_id):
        self.file_handler.save_id(new_id, constants.EM410X)

    def set_card(self, new_id):
        self.card_id = new_id
        self.print_card()
        self.write_to_card_button.set_enabled(True)

    def set_settings(self, settings):
        self.settings = settings
        if self.card_id != "":
            self.print_card()
