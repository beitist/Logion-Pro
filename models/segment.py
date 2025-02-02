from database.database_manager import DatabaseManager

class Segment:
    def __init__(self, section_id: int, source_text: str, translated_text: str = ""):
        self.section_id = section_id
        self.source_text = source_text
        self.translated_text = translated_text

    def save(self, db: DatabaseManager):
        return db.execute_query("INSERT INTO segments (section_id, source_text, translated_text) VALUES (?, ?, ?)", (self.section_id, self.source_text, self.translated_text))
