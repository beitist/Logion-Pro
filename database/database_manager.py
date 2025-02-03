import sqlite3
from typing import List, Optional

# Database Manager
class DatabaseManager:
    def __init__(self, db_path="logion.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def execute_query(self, query: str, params: tuple = ()):  
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor.lastrowid

    def fetch_all(self, query: str, params: tuple = ()) -> List[tuple]:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()