import sys
import os
from PyQt6.QtWidgets import QApplication
from logion_gui import ProjectManager
import sqlite3
from utils.docx_parser import DocxParser

def test_database():
    """Testet die Verbindung zur Datenbank."""
    conn = sqlite3.connect("logion.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    print("Vorhandene Tabellen:", tables)


def test_docx_parser():
    """Testet den DocxParser mit einer Beispiel-Datei."""
    file_path = os.path.join("test", "TR-sample.docx")
    if not os.path.exists(file_path):
        print(f"Fehler: Datei {file_path} nicht gefunden!")
        return
    
    print("\n🔍 Lade und analysiere Datei:", file_path)
    parser = DocxParser(file_path, section_divider=2)
    
    print("\n📌 Extracted Sections:")
    for section in parser.extract_sections():
        print(f"  - {section['title']} ({len(section['content'])} Absätze)")
    
    print("\n📌 Extracted Segments:")
    segments = parser.extract_segments()
    for section in segments:
        print(f"\n### {section['title']} ###")
        for sentence in section["content"]:
            print(f"  • {sentence}")

    print("\n📌 XML Structure:")
    xml_structure = parser.extract_xml_structure()
    print(xml_structure)


if __name__ == "__main__":
    print("Starte Logion...")
    test_database()
    test_docx_parser()
    
    app = QApplication(sys.argv)
    window = ProjectManager()
    window.show()
    sys.exit(app.exec())