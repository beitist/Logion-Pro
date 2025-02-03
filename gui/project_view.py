import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QLabel

class ProjectView(QWidget):
    def __init__(self):
        super().__init__()
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
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Projektname"])
        self.layout.addWidget(self.table)
        
        self.delete_button = QPushButton("Projekt löschen")
        self.delete_button.clicked.connect(self.delete_project)
        self.layout.addWidget(self.delete_button)
        
        self.setLayout(self.layout)
        self.load_projects()
    
    def load_projects(self):
        """Lädt die vorhandenen Projekte aus der Datenbank."""
        conn = sqlite3.connect("logion.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM projects")
        rows = cursor.fetchall()
        conn.close()
        
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(i, 1, QTableWidgetItem(row[1]))
    
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
    
    def delete_project(self):
        """Löscht das ausgewählte Projekt."""
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Fehler", "Bitte ein Projekt zum Löschen auswählen!")
            return
        
        project_id = self.table.item(selected, 0).text()
        conn = sqlite3.connect("logion.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        conn.close()
        
        self.load_projects()