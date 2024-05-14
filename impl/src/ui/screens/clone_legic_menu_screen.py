import logging
import os

from PyQt5.QtWidgets import QHBoxLayout

import constants

from ..buttons import CustomButton
from ..output_window import OutputWindow
from ..toast import InfoToast
from .base_screen import BaseScreen
from .clone_legic_select_screen import CloneLegicSelectScreen


class CloneLegicMenuScreen(BaseScreen):
    def __init__(self, command_builder, logger, stacked_widget, file_handler, parent=None):
        super().__init__(command_builder, logger, stacked_widget, file_handler, parent)
        self.dump_file = ""

        # Init of toasts
        self.add_toast("card_loaded", InfoToast(text="Legic card loaded.", duration=1.5, parent=self.stacked_widget))
        self.add_toast("loading", InfoToast(text="Loading...", duration=120, parent=self.stacked_widget))
        self.add_toast("writing", InfoToast(text="Writing...", duration=120, parent=self.stacked_widget))
        self.add_toast("write_sent", InfoToast(text="Write signal has been sent. Verify by loading.", duration=1.5, parent=self.stacked_widget))

    def add_screens_to_stacked_widget(self):
        # Init of screens
        self.clone_legic_select_screen = CloneLegicSelectScreen(self.command_builder, self.logger, self.stacked_widget, self.file_handler, self)

        # Adding them to the stacked widget
        self.stacked_widget.addWidget(self.clone_legic_select_screen)

    def setup_content(self):
        self.info_label = OutputWindow(self)
        self.hbox = QHBoxLayout()
        self.load_card_button = CustomButton("Load card", self.load_legic_card)
        self.select_saved_card_button = CustomButton("Select saved card", self.to_select_screen)
        self.write_to_card_button = CustomButton("Write to card", self.write_to_card)
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))

        self.print_info()
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

    def load_legic_card(self):
        self.show_toast("loading")
        self.run_command(constants.LOAD_LEGIC_CARD)

    def write_to_card(self):
        self.show_toast("writing")
        path_to_file = os.path.join(constants.DUMPS, constants.LEGIC_PRIME, self.dump_file)
        self.run_command(constants.WRITE_LEGIC_CARD, path_to_file)

    def to_select_screen(self):
        self.clone_legic_select_screen.refresh()
        self.switch_to_screen(self.clone_legic_select_screen)

    def react(self, command_name):
        if command_name == constants.LOAD_LEGIC_CARD:
            self.hide_toasts()
            self.dump_file = self.command_builder.get_output()
            self.set_card(self.dump_file)
            self.save_card()
            self.show_toast("card_loaded")
            self.logger.log(f"Loaded {self.dump_file}", level=logging.INFO)
        elif command_name == constants.WRITE_LEGIC_CARD:
            self.hide_toasts()
            self.show_toast("write_sent")
        else:
            self.logger.log(f"{__name__} encountered unknown command_name.", level=logging.WARNING)

    def print_info(self):
        self.info_label.set_text("Cached card info:\nLoad card or select from saved dump files to proceed.")

    def print_card(self):
        self.info_label.set_text(f"Cached card info:\nDump file: {self.dump_file}\n")

    def save_card(self):
        self.file_handler.move_dump_file(self.dump_file, constants.LEGIC_PRIME)

    def set_card(self, dump_file):
        self.dump_file = dump_file
        self.print_card()
        self.write_to_card_button.set_enabled(True)

    def set_settings(self, settings):
        self.settings = settings
        if self.card.get_id() != "":
            self.print_card()
