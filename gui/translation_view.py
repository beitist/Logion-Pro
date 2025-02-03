# gui/translation_view.py
from PyQt6.QtWidgets import QWidget

class TranslationView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Übersetzung")