import logging
import os

from PyQt5.QtWidgets import QHBoxLayout

import constants

from ..buttons import CustomButton
from ..output_window import OutputWindow
from ..toast import InfoToast
from .base_screen import BaseScreen
from .emulate_mf_ultralight_select_screen import \
    EmulateMFUltralightSelectScreen
from .emulate_mf_ultralight_settings_screen import \
    EmulateMFUltralightSettingsScreen


class EmulateMFUltralightMenuScreen(BaseScreen):
    def __init__(self, command_builder, logger, stacked_widget, file_handler, parent=None):
        self.dump_file = ""

        # Settings options
        self.settings = constants.MFU  # Default settings

        super().__init__(command_builder, logger, stacked_widget, file_handler, parent)

        # Init of toasts
        self.add_toast("card_loaded", InfoToast(text="Loading successful.", duration=1.5, parent=self.stacked_widget))
        self.add_toast("card_eloaded", InfoToast(text="Loading to emulator memory successful.", duration=1.5, parent=self.stacked_widget))
        self.add_toast("loading", InfoToast(text="Loading...", duration=constants.TOAST_DISAPPEAR_PERIOD, parent=self.stacked_widget))
        self.add_toast(
            "eloading",
            InfoToast(
                text="Loading to emulator memory.",
                duration=constants.TOAST_DISAPPEAR_PERIOD,
                parent=self.stacked_widget))
        self.add_toast(
            "emulation_progress",
            InfoToast(
                text="Emulating card. Press button to stop.",
                duration=constants.TOAST_DISAPPEAR_PERIOD,
                parent=self.stacked_widget))
        self.add_toast("emulation_stop", InfoToast(text="Emulating was stopped", duration=1.5, parent=self.stacked_widget))

    def add_screens_to_stacked_widget(self):
        # Init of screens
        self.emulate_mf_ultralight_settings_screen = EmulateMFUltralightSettingsScreen(
            self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)
        self.emulate_mf_ultralight_select_screen = EmulateMFUltralightSelectScreen(
            self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)

        # Adding them to the stacked widget
        self.stacked_widget.addWidget(self.emulate_mf_ultralight_settings_screen)
        self.stacked_widget.addWidget(self.emulate_mf_ultralight_select_screen)

    def setup_content(self):
        self.info_label = OutputWindow(self)
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.load_card_button = CustomButton("Read and save card", self.load_mf_ultralight_card)
        self.select_saved_card_button = CustomButton("Select source dump file", self.to_select_source_screen)

        self.emulate_card_button = CustomButton("Emulate card", self.emulate_card)
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))
        self.settings_button = CustomButton("⚙️ Settings", lambda: self.switch_to_screen(self.emulate_mf_ultralight_settings_screen))

        self.print_card()
        self.emulate_card_button.set_enabled(False)

        self.hbox1.addWidget(self.select_saved_card_button)
        self.hbox1.addWidget(self.emulate_card_button)
        self.hbox2.addWidget(self.back_button)
        self.hbox2.addWidget(self.settings_button)

        self.layout.addWidget(self.info_label)
        self.layout.addWidget(self.load_card_button)
        self.layout.addLayout(self.hbox1)
        self.layout.addLayout(self.hbox2)

        self.layout.setStretch(0, 1)

    def set_all_buttons_enabled(self, enabled):
        self.load_card_button.set_enabled(enabled)
        self.select_saved_card_button.set_enabled(enabled)
        self.back_button.set_enabled(enabled)
        self.settings_button.set_enabled(enabled)

        if self.dump_file != "":
            self.emulate_card_button.set_enabled(enabled)

    def stop_emulation(self):
        self.logger.log("Stopping the emulation", level=logging.INFO)
        self.hide_toasts()
        self.show_toast("emulation_stop")

    def load_mf_ultralight_card(self):
        self.show_toast("loading")
        self.run_command(constants.LOAD_MF_ULTRALIGHT_CARD)

    def emulate_card(self):
        self.show_toast("emulation_progress")
        self.logger.log(f"Starting simulation for {self.settings} tag.", level=logging.INFO)

        if self.settings == constants.MFU:
            self.run_command(constants.EMULATE_MF_ULTRALIGHT_CARD, ' -t 2 ')
        elif self.settings == constants.MFU_EV1:
            self.run_command(constants.EMULATE_MF_ULTRALIGHT_CARD, ' -t 7')
        else:
            self.logger.log(f"Writing to {self.settings} card encountered unknown settings.", level=logging.WARNING)

    def to_select_source_screen(self):
        self.emulate_mf_ultralight_select_screen.refresh()
        self.switch_to_screen(self.emulate_mf_ultralight_select_screen)

    def react(self, command_name):
        if command_name == constants.LOAD_MF_ULTRALIGHT_CARD:
            self.hide_toasts()
            dump = self.command_builder.get_output()
            self.save_card(dump)
            self.show_toast("card_loaded")
            self.logger.log(f"Saved dump file: {dump} ", level=logging.INFO)
        elif command_name == constants.ELOAD_MF_ULTRALIGHT_CARD:
            self.hide_toasts()
            self.print_card()
            self.emulate_card_button.set_enabled(True)
            self.show_toast("card_eloaded")
        elif command_name == constants.EMULATE_MF_ULTRALIGHT_CARD:
            self.stop_emulation()
        else:
            self.logger.log(f"{__name__} encountered unknown command_name.", level=logging.WARNING)

    def print_info(self):
        self.info_label.set_text("Cached card info:\nLoad card or add own ID to proceed.")

    def print_card(self):
        dumpfile = self.dump_file
        if dumpfile == "":
            dumpfile = "Select source dumpfile"
        self.info_label.set_text(
            f"Card info:\nSource dump file: {dumpfile}\nEmulation settings: {self.settings}\n")

    def save_card(self, dump_file):
        self.file_handler.move_dump_file(dump_file, constants.MF_ULTRALIGHT)

    def eload_mf_ultralight_card(self, dump_file):
        self.show_toast("eloading")
        self.logger.log(f"ELOADING with {dump_file}", level=logging.WARNING)

        path_to_dump_file = os.path.join(constants.DUMPS, constants.MF_ULTRALIGHT, dump_file)

        self.run_command(constants.ELOAD_MF_ULTRALIGHT_CARD, ' -f ' + path_to_dump_file)

    def set_source_card(self, dump_file):
        self.dump_file = dump_file
        self.eload_mf_ultralight_card(dump_file)

    def set_settings(self, settings):
        self.settings = settings
        self.print_card()
