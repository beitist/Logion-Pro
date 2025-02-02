class Project:
    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description

    def save(self, db: DatabaseManager):
        return db.execute_query("INSERT INTO projects (name, description) VALUES (?, ?)", (self.name, self.description))
