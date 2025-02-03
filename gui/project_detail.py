# gui/project_detail.py
from PyQt6.QtWidgets import QWidget

class ProjectDetailView(QWidget):
    def __init__(self, project_id=None):
        super().__init__()
        self.setWindowTitle("Projekt-Details")