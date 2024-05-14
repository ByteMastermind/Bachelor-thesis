import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QScrollArea, QSizePolicy, QSpacerItem,
                             QVBoxLayout, QWidget)

import constants

from ..buttons import CustomButton
from ..description import Description
from ..toast import InfoToast
from .base_screen import BaseScreen


class CloneLegicSelectScreen(BaseScreen):
    def __init__(self, command_builder, logger, stacked_widget, file_handler, parent=None):
        super().__init__(command_builder, logger, stacked_widget, file_handler, parent)

        # Init of toasts
        self.add_toast("success", InfoToast(text="Card successfully set.", duration=1.5, parent=self.stacked_widget))

    def setup_content(self):
        self.description_label = Description("Select Legic Prime card:")
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.button_layout = QVBoxLayout()

        self.load_from_files()

        self.scroll_area.setWidget(QWidget())
        self.scroll_area.widget().setLayout(self.button_layout)
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))

        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignBottom)

    def refresh(self):
        self.clear_layout(self.button_layout)
        self.load_from_files()
        self.logger.log(f"Updated the {constants.LEGIC_PRIME} files list.", level=logging.INFO)

    def load_from_files(self):
        self.filenames = self.file_handler.get_card_dumps(constants.LEGIC_PRIME)
        self.buttons = []
        for filename in self.filenames:
            self.buttons.append(CustomButton(filename))
            self.buttons[-1].clicked.connect(lambda _, filename=filename: self.select_file(filename))

        for button in self.buttons:
            self.button_layout.addWidget(button)

        # Add a stretchable spacer item to push buttons to the top
        self.spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.button_layout.addItem(self.spacer_item)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def select_file(self, filename):
        self.parent_screen.set_card(filename)
        self.show_toast("success")
        self.logger.log(f"Selected {filename} from {constants.LEGIC_PRIME} files list.", level=logging.INFO)
