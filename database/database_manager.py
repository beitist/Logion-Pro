import sqlite3
from typing import List, Optional

# Database Manager
class DatabaseManager:
    def __init__(self, db_path="logion.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
        """)
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS project_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            filename TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
        """)
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_file_id INTEGER,
            title TEXT NOT NULL,
            level INTEGER,
            FOREIGN KEY (project_file_id) REFERENCES project_files(id)
        )
        """)
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS segments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section_id INTEGER,
            source_text TEXT NOT NULL,
            translated_text TEXT,
            FOREIGN KEY (section_id) REFERENCES sections(id)
        )
        """)
        
        self.connection.commit()

    def execute_query(self, query: str, params: tuple = ()):  
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor.lastrowid

    def fetch_all(self, query: str, params: tuple = ()) -> List[tuple]:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()