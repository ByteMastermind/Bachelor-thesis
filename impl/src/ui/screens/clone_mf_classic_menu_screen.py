import logging
import os

from PyQt5.QtWidgets import QHBoxLayout

import constants

from ..buttons import CustomButton
from ..output_window import OutputWindow
from ..toast import InfoToast
from .base_screen import BaseScreen
from .clone_mf_classic_select_source_screen import \
    CloneMFClassicSelectSourceScreen
from .clone_mf_classic_select_target_screen import \
    CloneMFClassicSelectTargetScreen
from .clone_mf_classic_settings_screen import CloneMFClassicSettingsScreen


class CloneMFClassicMenuScreen(BaseScreen):
    def __init__(self, command_builder, logger, stacked_widget, file_handler, parent=None):
        self.source_card_dump_file = ""
        self.dest_card_keys_file = ""

        # Settings options
        self.settings = constants.MF_CLASSIC_1K  # Default settings

        super().__init__(command_builder, logger, stacked_widget, file_handler, parent)

        # Init of toasts
        self.add_toast("card_loaded", InfoToast(text="Key and dump file saved.", duration=1.5, parent=self.stacked_widget))
        self.add_toast("loading", InfoToast(text="Loading...", duration=constants.TOAST_DISAPPEAR_PERIOD, parent=self.stacked_widget))
        self.add_toast("writing", InfoToast(text="Writing...", duration=constants.TOAST_DISAPPEAR_PERIOD, parent=self.stacked_widget))
        self.add_toast("write_sent", InfoToast(text="Write signal has been sent. Verify by loading.", duration=1.5, parent=self.stacked_widget))

    def add_screens_to_stacked_widget(self):
        # Init of screens
        self.clone_mf_classic_settings_screen = CloneMFClassicSettingsScreen(
            self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)
        self.clone_mf_classic_select_source_screen = CloneMFClassicSelectSourceScreen(
            self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)
        self.clone_mf_classic_select_target_screen = CloneMFClassicSelectTargetScreen(
            self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)

        # Adding them to the stacked widget
        self.stacked_widget.addWidget(self.clone_mf_classic_settings_screen)
        self.stacked_widget.addWidget(self.clone_mf_classic_select_source_screen)
        self.stacked_widget.addWidget(self.clone_mf_classic_select_target_screen)

    def setup_content(self):
        self.info_label = OutputWindow(self)
        self.hbox = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.load_card_button = CustomButton("Load card", self.load_mf_card)
        self.select_saved_card_button = CustomButton("Select source dump file", self.to_select_source_screen)
        self.select_dest_keys_button = CustomButton("Select target card keys", self.to_select_target_screen)
        self.write_to_card_button = CustomButton("Write to card", self.write_to_card)
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))
        self.settings_button = CustomButton("⚙️ Settings", lambda: self.switch_to_screen(self.clone_mf_classic_settings_screen))

        self.print_card()
        self.write_to_card_button.set_enabled(False)

        self.hbox.addWidget(self.select_saved_card_button)
        self.hbox.addWidget(self.select_dest_keys_button)
        self.hbox1.addWidget(self.load_card_button)
        self.hbox1.addWidget(self.write_to_card_button)
        self.hbox2.addWidget(self.back_button)
        self.hbox2.addWidget(self.settings_button)

        self.layout.addWidget(self.info_label)
        self.layout.addLayout(self.hbox)
        self.layout.addLayout(self.hbox1)
        self.layout.addLayout(self.hbox2)

        self.layout.setStretch(0, 1)

    def set_all_buttons_enabled(self, enabled):
        self.load_card_button.set_enabled(enabled)
        self.select_saved_card_button.set_enabled(enabled)
        self.select_dest_keys_button.set_enabled(enabled)
        self.back_button.set_enabled(enabled)
        self.settings_button.set_enabled(enabled)

        if self.source_card_dump_file != "" and self.dest_card_keys_file != "":
            self.write_to_card_button.set_enabled(enabled)

    def load_mf_card(self):
        self.show_toast("loading")
        if self.settings == constants.MF_CLASSIC_1K:
            self.run_command(constants.AUTOPWN_MF_CARD, ' --1k')
        elif self.settings == constants.MF_CLASSIC_2K:
            self.run_command(constants.AUTOPWN_MF_CARD, ' --2k')
        elif self.settings == constants.MF_CLASSIC_4K:
            self.run_command(constants.AUTOPWN_MF_CARD, ' --4k')
        elif self.settings == constants.MF_CLASSIC_MINI:
            self.run_command(constants.AUTOPWN_MF_CARD, ' --mini')

    def write_to_card(self):
        self.show_toast("writing")
        path_to_dump_file = os.path.join(constants.DUMPS, self.settings, self.source_card_dump_file)
        path_to_keys_file = os.path.join(constants.KEYS, self.settings, self.dest_card_keys_file)

        if self.settings == constants.MF_CLASSIC_1K:
            self.run_command(constants.WRITE_MF_CARD, ' --1k ' + ' -f ' + path_to_dump_file + ' -k ' + path_to_keys_file)
        elif self.settings == constants.MF_CLASSIC_2K:
            self.run_command(constants.WRITE_MF_CARD, ' --2k ' + ' -f ' + path_to_dump_file + ' -k ' + path_to_keys_file)
        elif self.settings == constants.MF_CLASSIC_4K:
            self.run_command(constants.WRITE_MF_CARD, ' --4k ' + ' -f ' + path_to_dump_file + ' -k ' + path_to_keys_file)
        elif self.settings == constants.MF_CLASSIC_MINI:
            self.run_command(constants.WRITE_MF_CARD, ' --mini ' + ' -f ' + path_to_dump_file + ' -k ' + path_to_keys_file)
        else:
            self.logger.log(f"Writing to {self.settings} card encountered unknown settings.", level=logging.WARNING)

    def to_select_source_screen(self):
        self.clone_mf_classic_select_source_screen.refresh()
        self.switch_to_screen(self.clone_mf_classic_select_source_screen)

    def to_select_target_screen(self):
        self.clone_mf_classic_select_target_screen.refresh()
        self.switch_to_screen(self.clone_mf_classic_select_target_screen)

    def react(self, command_name):
        if command_name == constants.AUTOPWN_MF_CARD:
            self.hide_toasts()
            keys, dump = self.command_builder.get_output()
            self.set_source_card(dump)
            self.save_card(keys, dump)
            self.show_toast("card_loaded")
            self.logger.log(f"Saved keys file: {keys} and dump file: {dump} ", level=logging.INFO)
        elif command_name == constants.WRITE_MF_CARD:
            self.hide_toasts()
            self.show_toast("write_sent")
        else:
            self.logger.log(f"{__name__} encountered unknown command_name.", level=logging.WARNING)

    def print_info(self):
        self.info_label.set_text("Cached card info:\nLoad card or add own ID to proceed.")

    def print_card(self):
        dumpfile = self.source_card_dump_file
        dest_keyfile = self.dest_card_keys_file
        if dumpfile == "":
            dumpfile = "Select source dumpfile"
        if dest_keyfile == "":
            dest_keyfile = "Select destination keyfile"
        self.info_label.set_text(
            f"Card info:\nSource dump file: {dumpfile}\nDestination key file: {dest_keyfile}\nWrite settings: {self.settings}")

    def save_card(self, keys_file, dump_file):
        self.file_handler.move_dump_file(dump_file, self.settings)
        self.file_handler.move_keys_file(keys_file, self.settings)

    def set_source_card(self, dump_file):
        self.source_card_dump_file = dump_file
        self.print_card()
        if self.dest_card_keys_file != "" and self.source_card_dump_file != "":
            self.write_to_card_button.set_enabled(True)

    def set_dest_card(self, keys_file):
        self.dest_card_keys_file = keys_file
        self.print_card()
        if self.dest_card_keys_file != "" and self.source_card_dump_file != "":
            self.write_to_card_button.set_enabled(True)

    def set_settings(self, settings):
        self.settings = settings
        self.clone_mf_classic_select_source_screen.set_settings(settings)
        self.clone_mf_classic_select_target_screen.set_settings(settings)
        self.source_card_dump_file = ""
        self.dest_card_keys_file = ""
        self.write_to_card_button.set_enabled(False)
        self.print_card()
