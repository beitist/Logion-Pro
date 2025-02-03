import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QLabel, QHBoxLayout

class ProjectView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Projektverwaltung")
        self.layout = QVBoxLayout()
        
        self.label = QLabel("Projektname:")
        self.layout.addWidget(self.label)
        
        self.project_input = QLineEdit()
        self.layout.addWidget(self.project_input)
        
        self.add_button = QPushButton("Projekt hinzufügen")
        self.add_button.clicked.connect(self.add_project)
        self.layout.addWidget(self.add_button)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)  # Neue Spalte für das Lupen-Symbol
        self.table.setHorizontalHeaderLabels(["ID", "Projektname", "🔍"])
        self.layout.addWidget(self.table)
        
        self.setLayout(self.layout)
        self.load_projects()
    
    def load_projects(self):
        """Lädt die vorhandenen Projekte aus der Datenbank und zeigt sie in der Tabelle an."""
        conn = sqlite3.connect("logion.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM projects")
        rows = cursor.fetchall()
        conn.close()
        
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(i, 1, QTableWidgetItem(row[1]))

            # 🔍 Button zum Öffnen des Projekts
            btn_open = QPushButton("🔍")
            btn_open.clicked.connect(lambda checked, project_id=row[0]: self.open_project_details(project_id))
            self.table.setCellWidget(i, 2, btn_open)

    def add_project(self):
        """Fügt ein neues Projekt hinzu."""
        name = self.project_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Fehler", "Projektname darf nicht leer sein!")
            return
        
        conn = sqlite3.connect("logion.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO projects (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        
        self.project_input.clear()
        self.load_projects()
    
    def open_project_details(self, project_id):
        """Ruft die MainWindow-Funktion auf, um das Projekt zu öffnen."""
        main_window = self.window()  # Sucht das Hauptfenster (MainWindow)
        if hasattr(main_window, "open_project_details"):  # Prüft, ob Methode existiert
            main_window.open_project_details(project_id)