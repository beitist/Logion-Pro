from database.database_manager import DatabaseManager

class Project:
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

    def save(self, db: DatabaseManager):
        return db.execute_query("INSERT INTO projects (name, description) VALUES (?, ?)", (self.name, self.description))
