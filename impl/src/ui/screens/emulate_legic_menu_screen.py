import logging
import os

from PyQt5.QtWidgets import QHBoxLayout

import constants

from ..buttons import CustomButton
from ..output_window import OutputWindow
from ..toast import InfoToast
from .base_screen import BaseScreen
from .emulate_legic_select_screen import EmulateLegicSelectScreen
from .emulate_legic_settings_screen import EmulateLegicSettingsScreen


class EmulateLegicMenuScreen(BaseScreen):
    def __init__(self, command_builder, logger, stacked_widget, file_handler, parent=None):
        super().__init__(command_builder, logger, stacked_widget, file_handler, parent)
        self.dump_file = ""

        # Init of toasts
        self.add_toast("card_loaded", InfoToast(text="Legic card loaded.", duration=1.5, parent=self.stacked_widget))
        self.add_toast("loading", InfoToast(text="Loading...", duration=constants.TOAST_DISAPPEAR_PERIOD, parent=self.stacked_widget))
        self.add_toast(
            "eloading",
            InfoToast(
                text="Loading to emulator memory.",
                duration=constants.TOAST_DISAPPEAR_PERIOD,
                parent=self.stacked_widget))
        self.add_toast("card_eloaded", InfoToast(text="Loading to emulator memory successful.", duration=1.5, parent=self.stacked_widget))
        self.add_toast(
            "emulation_progress",
            InfoToast(
                text="Emulating card. Press button to stop.",
                duration=constants.TOAST_DISAPPEAR_PERIOD,
                parent=self.stacked_widget))
        self.add_toast("emulation_stop", InfoToast(text="Emulating was stopped", duration=1.5, parent=self.stacked_widget))

        # Settings options
        self.settings = constants.MIM256  # Default settings

    def add_screens_to_stacked_widget(self):
        # Init of screens
        self.emulate_legic_select_screen = EmulateLegicSelectScreen(self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)
        self.emulate_legic_settings_screen = EmulateLegicSettingsScreen(
            self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)

        # Adding them to the stacked widget
        self.stacked_widget.addWidget(self.emulate_legic_select_screen)
        self.stacked_widget.addWidget(self.emulate_legic_settings_screen)

    def setup_content(self):
        self.info_label = OutputWindow(self)
        self.hbox = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.load_card_button = CustomButton("Read and save card", self.load_legic_card)
        self.select_saved_card_button = CustomButton("Select saved card", self.to_select_screen)
        self.emulate_card_button = CustomButton("Emulate card", self.emulate_card)
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))
        self.settings_button = CustomButton("⚙️ Settings", lambda: self.switch_to_screen(self.emulate_legic_settings_screen))

        self.print_info()
        self.emulate_card_button.set_enabled(False)

        self.hbox.addWidget(self.select_saved_card_button)
        self.hbox.addWidget(self.emulate_card_button)
        self.hbox1.addWidget(self.back_button)
        self.hbox1.addWidget(self.settings_button)

        self.layout.addWidget(self.info_label)
        self.layout.addWidget(self.load_card_button)
        self.layout.addLayout(self.hbox)
        self.layout.addLayout(self.hbox1)

        self.layout.setStretch(0, 1)

    def set_all_buttons_enabled(self, enabled):
        self.load_card_button.set_enabled(enabled)
        self.select_saved_card_button.set_enabled(enabled)
        self.back_button.set_enabled(enabled)
        self.settings_button.set_enabled(enabled)

        if self.dump_file != "":
            self.emulate_card_button.set_enabled(enabled)

    def load_legic_card(self):
        self.show_toast("loading")
        self.run_command(constants.LOAD_LEGIC_CARD)

    def emulate_card(self):
        self.show_toast("emulation_progress")
        self.logger.log(f"Starting simulation for {self.settings} Legic Prime tag.", level=logging.INFO)
        if self.settings == constants.MIM22:
            self.run_command(constants.EMULATE_LEGIC_CARD, '--22')
        elif self.settings == constants.MIM256:
            self.run_command(constants.EMULATE_LEGIC_CARD, '--256')
        elif self.settings == constants.MIM1024:
            self.run_command(constants.EMULATE_LEGIC_CARD, '--1024')
        else:
            self.logger.log(f"Unknown settings {self.settings} encoutered", level=logging.WARNING)

    def eload_card(self, dump_file):
        if dump_file == "":
            self.logger.log("No loaded dumpfile. Not procceeding with action.", level=logging.WARNING)
            return
        self.show_toast("eloading")
        path_to_file = os.path.join(constants.DUMPS, constants.LEGIC_PRIME, self.dump_file)
        self.run_command(constants.ELOAD_LEGIC_CARD, path_to_file)

    def to_select_screen(self):
        self.emulate_legic_select_screen.refresh()
        self.switch_to_screen(self.emulate_legic_select_screen)

    def stop_emulation(self):
        self.logger.log("Stopping the simulation", level=logging.INFO)
        self.hide_toasts()
        self.show_toast("emulation_stop")

    def react(self, command_name):
        if command_name == constants.LOAD_LEGIC_CARD:
            self.hide_toasts()
            self.dump_file = self.command_builder.get_output()
            self.save_card()
            self.show_toast("card_loaded")
            self.logger.log(f"Saved {self.dump_file}", level=logging.INFO)
        elif command_name == constants.ELOAD_LEGIC_CARD:
            self.hide_toasts()
            self.print_card()
            self.emulate_card_button.set_enabled(True)
            self.show_toast("card_eloaded")
            self.logger.log(f"Loaded {self.dump_file} to emulator memory", level=logging.INFO)
        elif command_name == constants.EMULATE_LEGIC_CARD:
            self.stop_emulation()
        else:
            self.logger.log(f"{__name__} encountered unknown command_name.", level=logging.WARNING)

    def print_info(self):
        self.info_label.set_text("Cached card info:\nRead and save card, select from saved dump files to proceed.")

    def print_card(self):
        self.info_label.set_text(f"Cached card info:\nDump file: {self.dump_file}\nSimulator settings: {self.settings}")

    def save_card(self):
        self.file_handler.move_dump_file(self.dump_file, constants.LEGIC_PRIME)

    def set_card(self, dump_file):
        self.dump_file = dump_file
        self.eload_card(dump_file)

    def set_settings(self, settings):
        self.settings = settings
        if self.dump_file != "":
            self.print_card()
