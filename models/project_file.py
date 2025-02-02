class ProjectFile:
    def __init__(self, project_id: int, filename: str):
        self.project_id = project_id
        self.filename = filename

    def save(self, db: DatabaseManager):
        return db.execute_query("INSERT INTO project_files (project_id, filename) VALUES (?, ?)", (self.project_id, self.filename))
