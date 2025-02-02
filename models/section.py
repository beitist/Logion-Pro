class Section:
    def __init__(self, project_file_id: int, title: str, level: int):
        self.project_file_id = project_file_id
        self.title = title
        self.level = level

    def save(self, db: DatabaseManager):
        return db.execute_query("INSERT INTO sections (project_file_id, title, level) VALUES (?, ?, ?)", (self.project_file_id, self.title, self.level))
