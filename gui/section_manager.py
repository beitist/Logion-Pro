# gui/section_manager.py
from PyQt6.QtWidgets import QWidget

class SectionManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sections verwalten")