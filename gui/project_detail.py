import os
import sqlite3
from PyQt6.QtWidgets import QListWidgetItem, QWidget, QProgressBar, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QMessageBox, QLabel
from utils.docx_parser import DocxParser

class ProjectDetailView(QWidget):
    def __init__(self, project_id):
        super().__init__()
        self.project_id = project_id
        self.init_ui()  # Stellt sicher, dass die UI geladen wird

    def init_ui(self):
        self.setWindowTitle("Projekt-Details")
        self.layout = QVBoxLayout()
        
        self.project_label = QLabel("Projekt: Unbekannt")
        self.layout.addWidget(self.project_label)
        
        self.file_list = QListWidget()
        self.layout.addWidget(self.file_list)

        # Fortschrittsbalken für Übersetzung
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)  # Startwert
        self.progress_label = QLabel("0/0 Segmente übersetzt")
        
        self.layout.addWidget(self.progress_label)
        self.layout.addWidget(self.progress_bar)
        
        # Buttons für Datei-Handling
        self.add_file_btn = QPushButton("📂 Datei hinzufügen")
        self.add_file_btn.clicked.connect(self.add_file)
        self.layout.addWidget(self.add_file_btn)

        self.remove_file_btn = QPushButton("🗑️ Datei entfernen")
        self.remove_file_btn.clicked.connect(self.remove_file)
        self.layout.addWidget(self.remove_file_btn)
        
        # Button zur Generierung der übersetzten Datei
        self.generate_translation_btn = QPushButton("📄 Übersetzte Datei generieren")
        self.generate_translation_btn.clicked.connect(self.generate_translated_file)
        self.layout.addWidget(self.generate_translation_btn)

        self.setLayout(self.layout)
    
    def update_project(self, project_id):
        """Aktualisiert die Ansicht mit dem neuen Projekt."""
        self.project_id = project_id
        project_name = self.get_project_name()
        self.project_label.setText(f"Projekt: {project_name}")
        self.load_files()
    
    def get_project_name(self):
        """Holt den Projektnamen aus der Datenbank."""
        conn = sqlite3.connect("logion.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM projects WHERE id = ?", (self.project_id,))
        project_name = cursor.fetchone()
        conn.close()
        return project_name[0] if project_name else "Unbekanntes Projekt"
    
    def load_files(self):
        """Lädt die Dateien des Projekts und macht sie anklickbar."""
        conn = sqlite3.connect("logion.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, filename FROM project_files WHERE project_id = ?", (self.project_id,))
        rows = cursor.fetchall()
        conn.close()

        self.file_list.clear()
        for row in rows:
            item = QListWidgetItem(row[1])
            item.setData(256, row[0])  # Speichert project_file_id im Item
            self.file_list.addItem(item)

        # Event für Klick auf eine Datei
        self.file_list.itemClicked.connect(lambda item: self.file_selected(item.data(256)))
        
    def add_file(self):
        """Öffnet einen Dialog zum Hinzufügen einer Datei."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Datei auswählen", "", "Word-Dateien (*.docx)")
        if not file_path:
            return
        
        filename = os.path.basename(file_path)
        conn = sqlite3.connect("logion.db")
        cursor = conn.cursor()
        
        # Datei in project_files speichern
        cursor.execute("INSERT INTO project_files (project_id, filename) VALUES (?, ?)", (self.project_id, filename))
        project_file_id = cursor.lastrowid  # ID der eingefügten Datei speichern
        
        # Datei analysieren
        parser = DocxParser(file_path)
        sections = parser.extract_sections()
        
        # Nutzer fragen, ob Sections genutzt werden sollen
        use_sections = QMessageBox.question(self, "Sections nutzen?", f"Diese Datei enthält {len(sections)} mögliche Sections. Möchtest du Sections nutzen?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if use_sections == QMessageBox.StandardButton.Yes:
            section_depth = QMessageBox.question(self, "Section-Tiefe", "Sollen nur Heading 1 oder auch Heading 2 als Sections genutzt werden?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            section_divider = 1 if section_depth == QMessageBox.StandardButton.No else 2
            
            # Sections speichern
            for section in sections:
                cursor.execute("INSERT INTO sections (project_file_id, title, level) VALUES (?, ?, ?)", (project_file_id, section["title"], section_divider))
                section_id = cursor.lastrowid  # Die ID der eingefügten Section holen
                
                # Segmente dieser Section speichern
                for sentence in section["content"]:
                    cursor.execute("INSERT INTO segments (section_id, source_text) VALUES (?, ?)", (section_id, sentence))
        
        else:
            # Eine einzelne Section für die Datei anlegen
            cursor.execute("INSERT INTO sections (project_file_id, title, level) VALUES (?, ?, ?)", (project_file_id, filename, 0))
            section_id = cursor.lastrowid
            
            # Alle Segmente aus der Datei speichern
            segments = parser.extract_segments()
            for sentence in segments:
                cursor.execute("INSERT INTO segments (section_id, source_text) VALUES (?, ?)", (section_id, sentence))
        
        conn.commit()  # Jetzt erst committen
        conn.close()   # Und dann schließen
        self.load_files()  # GUI aktualisieren
    
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

    def update_translation_progress(self, translated_segments, total_segments):
        """Aktualisiert den Fortschrittsbalken basierend auf übersetzten Segmenten."""
        if total_segments > 0:
            progress = int((translated_segments / total_segments) * 100)
        else:
            progress = 0
        
        self.progress_bar.setValue(progress)
        self.progress_label.setText(f"{translated_segments}/{total_segments} Segmente übersetzt")

    def generate_translated_file(self):
        """Platzhalter für die Funktion zur Generierung der übersetzten Datei."""
        QMessageBox.information(self, "Übersetzung", "Die übersetzte Datei wird generiert...")

    def file_selected(self, project_file_id):
        """Aktiviert den Section-Tab, wenn eine Datei ausgewählt wurde."""
        self.parent().open_section_manager(project_file_id)