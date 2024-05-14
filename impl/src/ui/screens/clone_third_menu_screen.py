from PyQt5.QtCore import Qt

from ..buttons import CustomButton
from .base_screen import BaseScreen


class CloneThirdMenuScreen(BaseScreen):
    def setup_content(self):
        self.back_button = CustomButton("⬅️ Back", lambda: self.switch_to_screen(self.parent_screen))

        self.layout.addWidget(self.back_button, alignment=Qt.AlignBottom)
