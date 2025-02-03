import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QMessageBox

class SegmentView(QWidget):
    def __init__(self, section_id):
        super().__init__()
        self.section_id = section_id
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Segmente-Übersicht")
        self.layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Original, Übersetzung, Speichern-Button
        self.table.setHorizontalHeaderLabels(["Original", "Übersetzung", ""])
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

            # Übersetzung als Textfeld (falls vorhanden)
            translation_input = QLineEdit()
            if row[2]:
                translation_input.setText(row[2])
            self.table.setCellWidget(i, 1, translation_input)

            # Speichern-Button
            btn_save = QPushButton("💾 Speichern")
            btn_save.clicked.connect(lambda checked, seg_id=row[0], input_field=translation_input: self.save_translation(seg_id, input_field))
            self.table.setCellWidget(i, 2, btn_save)
    
    def save_translation(self, segment_id, input_field):
        """Speichert die bearbeitete Übersetzung."""
        new_translation = input_field.text().strip()
        conn = sqlite3.connect("logion.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE segments SET translated_text = ? WHERE id = ?", (new_translation, segment_id))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Gespeichert", "Die Übersetzung wurde gespeichert.")