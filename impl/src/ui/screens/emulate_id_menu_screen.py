import logging

from PyQt5.QtWidgets import QHBoxLayout

import constants

from ..buttons import CustomButton
from ..output_window import OutputWindow
from ..toast import InfoToast
from .base_screen import BaseScreen
from .emulate_id_select_screen import EmulateIDSelectScreen
from .emulate_id_settings_screen import EmulateIDSettingsScreen
from .input_screen import InputScreen


class EmulateIDMenuScreen(BaseScreen):
    def __init__(self, command_builder, logger, stacked_widget, file_handler, parent=None):
        super().__init__(command_builder, logger, stacked_widget, file_handler, parent)
        self.card_id = ""

        # Init of toasts
        self.add_toast("id_loaded", InfoToast(text="Card ID loaded.", duration=1.5, parent=self.stacked_widget))
        self.add_toast("loading", InfoToast(text="Loading...", duration=constants.TOAST_DISAPPEAR_PERIOD, parent=self.stacked_widget))
        self.add_toast(
            "emulation_progress",
            InfoToast(
                text="Emulating card. Press button to stop.",
                duration=constants.TOAST_DISAPPEAR_PERIOD,
                parent=self.stacked_widget))
        self.add_toast("emulation_stop", InfoToast(text="Emulating was stopped", duration=1.5, parent=self.stacked_widget))

        # Settings options
        self.settings = constants.EM410X  # Default settings

    def add_screens_to_stacked_widget(self):
        # Init of screens
        self.emulate_id_input_screen = InputScreen(self.command_builder, self.logger, self.stacked_widget, self.file_handler, self, id_lengths=10)
        self.emulate_id_settings_screen = EmulateIDSettingsScreen(
            self.command_builder,
            self.logger,
            self.stacked_widget,
            self.file_handler,
            self,
            self.emulate_id_input_screen)
        self.emulate_id_select_screen = EmulateIDSelectScreen(self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)

        # Adding them to the stacked widget
        self.stacked_widget.addWidget(self.emulate_id_input_screen)
        self.stacked_widget.addWidget(self.emulate_id_settings_screen)
        self.stacked_widget.addWidget(self.emulate_id_select_screen)

    def setup_content(self):
        self.info_label = OutputWindow(self)
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.load_card_button = CustomButton("Load card", self.load_card)
        self.add_own_id_button = CustomButton("Add own ID", lambda: self.switch_to_screen(self.emulate_id_input_screen))
        self.select_saved_card_button = CustomButton("Select saved card", self.to_select_screen)
        self.emulate_card_button = CustomButton("Emulate card", self.emulate_card)
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))
        self.settings_button = CustomButton("⚙️ Settings", lambda: self.switch_to_screen(self.emulate_id_settings_screen))

        self.print_info()
        self.emulate_card_button.set_enabled(False)

        self.hbox1.addWidget(self.load_card_button)
        self.hbox1.addWidget(self.add_own_id_button)
        self.hbox2.addWidget(self.select_saved_card_button)
        self.hbox2.addWidget(self.emulate_card_button)
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
            self.emulate_card_button.set_enabled(enabled)

    def load_card(self):
        self.show_toast("loading")
        if self.settings == constants.EM410X:
            self.run_command(constants.LOAD_EM410X_ID)
        elif self.settings == constants.MF_CLASSIC_1K:
            self.run_command(constants.LOAD_MF_ID)
        elif self.settings == constants.MF_CLASSIC_4K:
            self.run_command(constants.LOAD_MF_ID)
        elif self.settings == constants.MF_DESFIRE:
            self.run_command(constants.LOAD_MF_ID)
        elif self.settings == constants.MF_ULTRALIGHT:
            self.run_command(constants.LOAD_MF_ID)
        else:
            self.logger.log(f"Unknown settings {self.settings} encoutered.", level=logging.WARNING)

    def emulate_card(self):
        self.show_toast("emulation_progress")
        self.logger.log(f"Starting simulation of {self.card_id} for {self.settings} tag.", level=logging.INFO)
        if self.settings == constants.EM410X:
            self.run_command(constants.EMULATE_EM410X_ID, self.card_id)
        elif self.settings == constants.MF_CLASSIC_1K:
            self.run_command(constants.EMULATE_MF_CLASSIC_1K_ID, self.card_id)
        elif self.settings == constants.MF_CLASSIC_4K:
            self.run_command(constants.EMULATE_MF_CLASSIC_4K_ID, self.card_id)
        elif self.settings == constants.MF_DESFIRE:
            self.run_command(constants.EMULATE_DESFIRE_ID, self.card_id)
        elif self.settings == constants.MF_ULTRALIGHT:
            self.run_command(constants.EMULATE_MF_ULTRALIGHT_ID, self.card_id)
        else:
            self.logger.log(f"Unknown settings {self.settings} encoutered", level=logging.WARNING)

    def stop_emulation(self):
        self.logger.log("Stopping the simulation", level=logging.INFO)
        self.hide_toasts()
        self.show_toast("emulation_stop")

    def to_select_screen(self):
        self.emulate_id_select_screen.refresh()
        self.switch_to_screen(self.emulate_id_select_screen)

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
        elif command_name == constants.LOAD_MF_ID:
            self.hide_toasts()
            new_id = self.command_builder.get_output()
            if len(new_id) not in (8, 10, 14):
                self.logger.log(f"Loaded ID {new_id} is unknown size.", level=logging.WARNING)
            self.set_card(new_id)
            self.save_card(new_id)
            self.show_toast("id_loaded")
            self.logger.log(f"Loaded ID {new_id}", level=logging.INFO)
        elif command_name in (constants.EMULATE_DESFIRE_ID, constants.EMULATE_MF_CLASSIC_1K_ID,
                              constants.EMULATE_MF_CLASSIC_4K_ID, constants.EMULATE_MF_ULTRALIGHT_ID,
                              constants.EMULATE_EM410X_ID):
            self.stop_emulation()
        else:
            self.logger.log(f"Encountered unknown command_name: {command_name}", level=logging.WARNING)

    def print_info(self):
        self.info_label.set_text("Cached card info:\nLoad card or add own ID to proceed.")

    def print_card(self):
        self.info_label.set_text(f"Card info:\nID: {self.card_id}\nTag type settings: {self.settings}")

    def set_settings(self, settings):
        self.settings = settings
        self.emulate_id_select_screen.set_settings(self.settings)
        if (self.settings == constants.EM410X and len(self.card_id) != 10) or (self.settings == constants.MF_DESFIRE and len(self.card_id) == 10):
            self.card_id = ""
            self.print_info()
            self.emulate_card_button.set_enabled(False)
            return
        if self.card_id != "":
            self.print_card()

    def set_card(self, new_id):
        self.card_id = new_id
        self.print_card()
        self.emulate_card_button.set_enabled(True)

    def save_card(self, card_id):
        self.file_handler.save_id(card_id, self.settings)

    def get_settings(self):
        return self.settings
