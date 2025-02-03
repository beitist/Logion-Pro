import os
import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QMessageBox, QLabel
from utils.docx_parser import DocxParser

class ProjectDetailView(QWidget):
    def __init__(self, project_id):
        super().__init__()
        self.project_id = project_id
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Projekt-Details")
        self.layout = QVBoxLayout()
        
        self.project_label = QLabel("Projekt: " + self.get_project_name())
        self.layout.addWidget(self.project_label)
        
        self.file_list = QListWidget()
        self.load_files()
        self.layout.addWidget(self.file_list)
        
        self.add_file_btn = QPushButton("📂 Datei hinzufügen")
        self.add_file_btn.clicked.connect(self.add_file)
        
        self.remove_file_btn = QPushButton("🗑️ Datei entfernen")
        self.remove_file_btn.clicked.connect(self.remove_file)
        
        self.layout.addWidget(self.add_file_btn)
        self.layout.addWidget(self.remove_file_btn)
        self.setLayout(self.layout)
    
    def get_project_name(self):
        """Holt den Projektnamen aus der Datenbank."""
        conn = sqlite3.connect("logion.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM projects WHERE id = ?", (self.project_id,))
        project_name = cursor.fetchone()
        conn.close()
        return project_name[0] if project_name else "Unbekanntes Projekt"
    
    def load_files(self):
        """Lädt die vorhandenen Dateien für das Projekt."""
        self.file_list.clear()
        conn = sqlite3.connect("logion.db")
        cursor = conn.cursor()
        cursor.execute("SELECT filename FROM project_files WHERE project_id = ?", (self.project_id,))
        files = cursor.fetchall()
        conn.close()
        for file in files:
            self.file_list.addItem(file[0])
    
    def add_file(self):
        """Öffnet einen Dialog zum Hinzufügen einer Datei."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Datei auswählen", "", "Word-Dateien (*.docx)")
        if not file_path:
            return
        
        filename = os.path.basename(file_path)
        conn = sqlite3.connect("logion.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO project_files (project_id, filename) VALUES (?, ?)", (self.project_id, filename))
        conn.commit()
        conn.close()
        
        # Datei analysieren
        parser = DocxParser(file_path)
        sections = parser.extract_sections()
        
        # Nutzer fragen, ob Sections genutzt werden sollen
        use_sections = QMessageBox.question(self, "Sections nutzen?", f"Diese Datei enthält {len(sections)} mögliche Sections. Möchtest du Sections nutzen?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if use_sections == QMessageBox.StandardButton.Yes:
            section_depth = QMessageBox.question(self, "Section-Tiefe", "Sollen nur Heading 1 oder auch Heading 2 als Sections genutzt werden?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            section_divider = 1 if section_depth == QMessageBox.StandardButton.No else 2
            
            # Sections speichern
            for section in parser.extract_sections():
                cursor.execute("INSERT INTO sections (project_file_id, title, level) VALUES (?, ?, ?)", (self.project_id, section["title"], section_divider))
        else:
            # Eine einzelne Section für die Datei anlegen
            cursor.execute("INSERT INTO sections (project_file_id, title, level) VALUES (?, ?, ?)", (self.project_id, filename, 0))
        
        conn.commit()
        conn.close()
        self.load_files()
    
    def remove_file(self):
        """Löscht eine Datei aus dem Projekt."""
        selected_item = self.file_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Fehler", "Bitte eine Datei auswählen, um sie zu entfernen.")
            return
        
        filename = selected_item.text()
        conn = sqlite3.connect("logion.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM project_files WHERE project_id = ? AND filename = ?", (self.project_id, filename))
        cursor.execute("DELETE FROM sections WHERE project_file_id = (SELECT id FROM project_files WHERE filename = ?)", (filename,))
        conn.commit()
        conn.close()
        self.load_files()