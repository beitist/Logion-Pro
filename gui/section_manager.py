import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
import sys
sys.path.append("gui")
from segment_view import SegmentView

class SectionManager(QWidget):
    def __init__(self, project_file_id):
        super().__init__()
        self.project_file_id = project_file_id
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Sections-Übersicht")
        self.layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Titel, Level, Button
        self.table.setHorizontalHeaderLabels(["Titel", "Level", "Segmente"])
        self.layout.addWidget(self.table)

        self.load_sections()
        self.setLayout(self.layout)
    
    def load_sections(self):
        """Lädt alle Sections für die Datei."""
        conn = sqlite3.connect("logion.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, level FROM sections WHERE project_file_id = ?", (self.project_file_id,))
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(row[1]))  # Titel
            self.table.setItem(i, 1, QTableWidgetItem(str(row[2])))  # Level

            # Button zum Öffnen der Segmente
            btn_open = QPushButton("🔍 Segmente")
            btn_open.clicked.connect(lambda checked, section_id=row[0]: self.open_segments(section_id))
            self.table.setCellWidget(i, 2, btn_open)
    
    def open_segments(self, section_id):
        """Öffnet die Segmente-Ansicht für eine Section."""
        self.segment_view = SegmentView(section_id)
        self.segment_view.show()