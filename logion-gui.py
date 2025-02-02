import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QLineEdit, QLabel

# Datenbank-Setup
def init_db():
    conn = sqlite3.connect("logion.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

class ProjectManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logion - Projektverwaltung")
        self.setGeometry(100, 100, 600, 400)
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

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = ProjectManager()
    window.show()
    sys.exit(app.exec())
