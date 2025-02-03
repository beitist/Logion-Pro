import sqlite3
import os

def initialize_database():
    if os.path.exists("logion.db"):
        print("✅ Datenbank existiert bereits.")
        return
    
    print("📌 Erstelle Datenbank und Tabellen...")
    conn = sqlite3.connect("logion.db")
    cursor = conn.cursor()
    
    # Projekte-Tabelle
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            customer TEXT DEFAULT '',
            summary TEXT DEFAULT ''
        )
    ''')
    
    # Dateien-Tabelle
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
        )
    ''')
    
    # Sections-Tabelle
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_file_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            level INTEGER NOT NULL,
            FOREIGN KEY (project_file_id) REFERENCES project_files(id) ON DELETE CASCADE
        )
    ''')

    # Segments-Tabelle
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS segments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section_id INTEGER NOT NULL,
            source_text TEXT NOT NULL,
            translated_text TEXT DEFAULT '',
            FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Datenbank wurde erfolgreich initialisiert.")

if __name__ == "__main__":
    initialize_database()
