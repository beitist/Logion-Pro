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
        
        # 📌 Tabs EINMAL erstellen
        self.project_view = ProjectView(self)
        self.project_detail = ProjectDetailView(None)  # Startet leer
        self.section_manager = SectionManager()
        self.translation_view = TranslationView()
        
        self.tabs.addTab(self.project_view, "📂 Projekte")
        self.tabs.addTab(self.project_detail, "📜 Projekt-Details")
        self.tabs.addTab(self.section_manager, "🔍 Sections")
        self.tabs.addTab(self.translation_view, "🌍 Übersetzung")
    
    def open_project_details(self, project_id):
        """Aktualisiert den bestehenden `ProjectDetailView` anstatt einen neuen Tab zu erstellen."""
        print(f"🔄 Wechsel zu Projekt-ID: {project_id}")  # Debugging
        
        self.project_detail.update_project(project_id)  # Aktualisiert den bestehenden Tab
        self.tabs.setCurrentIndex(1)  # Wechsel zu Projekt-Details-Tab

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()