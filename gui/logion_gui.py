import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from gui.project_view import ProjectView
from gui.project_detail import ProjectDetailView
from gui.section_manager import SectionManager
from gui.translation_view import TranslationView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logion - Übersetzungsmanagement")
        self.setGeometry(100, 100, 800, 600)
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Tabs hinzufügen
        self.project_view = ProjectView(self)
        self.project_detail = ProjectDetailView(None)  # Noch keine Projekt-ID zugewiesen
        self.section_manager = SectionManager()
        self.translation_view = TranslationView()
        
        self.tabs.addTab(self.project_view, "📂 Projekte")
        self.tabs.addTab(self.project_detail, "📜 Projekt-Details")
        self.tabs.addTab(self.section_manager, "🔍 Sections")
        self.tabs.addTab(self.translation_view, "🌍 Übersetzung")
    
    def open_project_details(self, project_id):
        """Öffnet die Projektdetailansicht für das gewählte Projekt."""
        self.project_detail = ProjectDetailView(project_id)
        self.tabs.removeTab(1)  # Entfernt alten Detail-Tab
        self.tabs.insertTab(1, self.project_detail, "📜 Projekt-Details")  # Fügt neuen ein
        self.tabs.setCurrentIndex(1)  # Springt zum Tab

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())