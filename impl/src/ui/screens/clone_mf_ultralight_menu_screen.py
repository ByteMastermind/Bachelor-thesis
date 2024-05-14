import logging
import os

from PyQt5.QtWidgets import QHBoxLayout

import constants

from ..buttons import CustomButton
from ..output_window import OutputWindow
from ..toast import InfoToast
from .base_screen import BaseScreen
from .clone_mf_ultralight_select_screen import CloneMFUltralightSelectScreen


class CloneMFUltralightMenuScreen(BaseScreen):
    def __init__(self, command_builder, logger, stacked_widget, file_handler, parent=None):
        self.dump_file = ""

        super().__init__(command_builder, logger, stacked_widget, file_handler, parent)

        # Init of toasts
        self.add_toast("card_loaded", InfoToast(text="Dump file saved.", duration=1.5, parent=self.stacked_widget))
        self.add_toast("loading", InfoToast(text="Loading...", duration=constants.TOAST_DISAPPEAR_PERIOD, parent=self.stacked_widget))
        self.add_toast("writing", InfoToast(text="Writing...", duration=constants.TOAST_DISAPPEAR_PERIOD, parent=self.stacked_widget))
        self.add_toast("write_sent", InfoToast(text="Write signal has been sent. Verify by loading.", duration=1.5, parent=self.stacked_widget))

    def add_screens_to_stacked_widget(self):
        # Init of screens
        self.clone_mf_ultralight_select_screen = CloneMFUltralightSelectScreen(
            self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)

        # Adding them to the stacked widget
        self.stacked_widget.addWidget(self.clone_mf_ultralight_select_screen)

    def setup_content(self):
        self.info_label = OutputWindow(self)
        self.hbox = QHBoxLayout()
        self.load_card_button = CustomButton("Load card", self.load_mf_ultralight_card)
        self.select_saved_card_button = CustomButton("Select source dump file", self.to_select_screen)
        self.write_to_card_button = CustomButton("Write to card", self.write_to_card)
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))

        self.print_card()
        self.write_to_card_button.set_enabled(False)

        self.hbox.addWidget(self.select_saved_card_button)
        self.hbox.addWidget(self.write_to_card_button)

        self.layout.addWidget(self.info_label)
        self.layout.addWidget(self.load_card_button)
        self.layout.addLayout(self.hbox)
        self.layout.addWidget(self.back_button)
        self.layout.setStretch(0, 1)

    def set_all_buttons_enabled(self, enabled):
        self.load_card_button.set_enabled(enabled)
        self.select_saved_card_button.set_enabled(enabled)
        self.back_button.set_enabled(enabled)

        if self.dump_file != "":
            self.write_to_card_button.set_enabled(enabled)

    def load_mf_ultralight_card(self):
        self.show_toast("loading")
        self.run_command(constants.LOAD_MF_ULTRALIGHT_CARD)

    def write_to_card(self):
        self.show_toast("writing")
        path_to_dump_file = os.path.join(constants.DUMPS, constants.MF_ULTRALIGHT, self.dump_file)

        self.run_command(constants.WRITE_MF_ULTRALIGHT_CARD, ' -f ' + path_to_dump_file)

    def to_select_screen(self):
        self.clone_mf_ultralight_select_screen.refresh()
        self.switch_to_screen(self.clone_mf_ultralight_select_screen)

    def react(self, command_name):
        if command_name == constants.LOAD_MF_ULTRALIGHT_CARD:
            self.hide_toasts()
            dump = self.command_builder.get_output()
            self.set_card(dump)
            self.save_card(dump)
            self.show_toast("card_loaded")
            self.logger.log(f"Saved dump file: {dump} ", level=logging.INFO)
        elif command_name == constants.WRITE_MF_ULTRALIGHT_CARD:
            self.hide_toasts()
            self.show_toast("write_sent")
        else:
            self.logger.log(f"{__name__} encountered unknown command_name.", level=logging.WARNING)

    def print_info(self):
        self.info_label.set_text("Cached card info:\nLoad card or add own ID to proceed.")

    def print_card(self):
        dump_file = self.dump_file
        if dump_file == "":
            dump_file = "Select source dumpfile"
        self.info_label.set_text(
            f"Ultralight card info:\nSource dump file: {dump_file}")

    def save_card(self, dump_file):
        self.file_handler.move_dump_file(dump_file, constants.MF_ULTRALIGHT)

    def set_card(self, dump_file):
        self.dump_file = dump_file
        self.print_card()
        self.write_to_card_button.set_enabled(True)
