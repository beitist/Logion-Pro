import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel

class SegmentView(QWidget):
    def __init__(self, section_id):
        super().__init__()
        self.section_id = section_id
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Segmente-Übersicht")
        self.layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Original, Übersetzung, MT/LLM-Buttons
        self.table.setHorizontalHeaderLabels(["Original Text", "Übersetzung", "MT/LLM"])
        self.layout.addWidget(self.table)

        self.load_segments()
        self.setLayout(self.layout)
    
    def load_segments(self):
        """Lädt alle Segmente für die Section."""
        conn = sqlite3.connect("logion.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, source_text, translated_text FROM segments WHERE section_id = ?", (self.section_id,))
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(row[1]))  # Originaltext

            # Übersetzung als Textfeld
            translation_input = QLineEdit()
            if row[2]:
                translation_input.setText(row[2])
            self.table.setCellWidget(i, 1, translation_input)

            # Buttons für MT & LLM
            btn_mt = QPushButton("🌍 MT")
            btn_llm = QPushButton("🤖 LLM")
            btn_mt.clicked.connect(lambda checked, seg_id=row[0], input_field=translation_input: self.apply_mt(seg_id, input_field))
            btn_llm.clicked.connect(lambda checked, seg_id=row[0], input_field=translation_input: self.apply_llm(seg_id, input_field))

            mt_llm_layout = QWidget()
            mt_llm_layout_layout = QVBoxLayout()
            mt_llm_layout_layout.addWidget(btn_mt)
            mt_llm_layout_layout.addWidget(btn_llm)
            mt_llm_layout.setLayout(mt_llm_layout_layout)
            self.table.setCellWidget(i, 2, mt_llm_layout)
    
    def apply_mt(self, segment_id, input_field):
        """Platzhalter für Machine Translation."""
        input_field.setText("MT-Ergebnis hier")  # TODO: Anbindung an MT-API

    def apply_llm(self, segment_id, input_field):
        """Platzhalter für LLM-gestützte Verbesserung."""
        input_field.setText("LLM-Verbesserung hier")  # TODO: Anbindung an LLM-API