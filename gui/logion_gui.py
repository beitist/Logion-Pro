from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget
from gui.project_view import ProjectView
from gui.project_detail import ProjectDetailView
from gui.section_manager import SectionManager
from gui.segment_view import SegmentView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logion - Übersetzungsmanagement")
        self.setGeometry(100, 100, 800, 600)
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # 📌 Tabs EINMAL erstellen, aber Sections & Segmente erst später aktivieren
        self.project_view = ProjectView(self)
        self.project_detail = ProjectDetailView(None)  # Startet leer
        self.section_manager = QWidget()  # Platzhalter, bis Projekt geöffnet wird
        self.segment_view = QWidget()  # Platzhalter, bis Section geöffnet wird

        self.tabs.addTab(self.project_view, "📂 Projekte")
        self.tabs.addTab(self.project_detail, "📜 Projekt-Details")
        self.section_manager_index = self.tabs.addTab(self.section_manager, "🔍 Sections")
        self.segment_view_index = self.tabs.addTab(self.segment_view, "🌍 Segmente/Übersetzung")

        # Sections & Segmente-Tab deaktivieren
        self.tabs.setTabEnabled(self.section_manager_index, False)
        self.tabs.setTabEnabled(self.segment_view_index, False)
    
    def open_project_details(self, project_id):
        """Aktualisiert den bestehenden `ProjectDetailView` anstatt einen neuen Tab zu erstellen."""
        print(f"🔄 Wechsel zu Projekt-ID: {project_id}")  # Debugging
        
        self.project_detail.update_project(project_id)  # Aktualisiert den bestehenden Tab
        self.tabs.setCurrentIndex(1)  # Wechsel zu Projekt-Details-Tab

    def open_section_manager(self, project_file_id):
        """Öffnet den Section-Manager für eine Datei."""
        if self.section_manager is not None:
            self.tabs.removeTab(self.section_manager_index)

        self.section_manager = SectionManager(project_file_id)
        self.section_manager_index = self.tabs.insertTab(2, self.section_manager, "🔍 Sections")
        self.tabs.setCurrentIndex(self.section_manager_index)

    def open_segment_view(self, section_id):
        """Öffnet die Segment-Ansicht für eine Section."""
        if self.segment_view is not None:
            self.tabs.removeTab(self.segment_view_index)

        self.segment_view = SegmentView(section_id)
        self.segment_view_index = self.tabs.insertTab(3, self.segment_view, "🌍 Segmente/Übersetzung")
        self.tabs.setCurrentIndex(self.segment_view_index)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()