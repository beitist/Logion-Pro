import re
from docx import Document
from typing import List, Dict, Tuple, Union
import xml.etree.ElementTree as ET

class DocxParser:
    def __init__(self, file_path: str, section_dividers: List[int] = [1]):
        """Initialisiert den Parser mit der Option, mehrere Heading-Levels als Section-Start zu nutzen."""
        self.file_path = file_path
        self.section_dividers = section_dividers  # Standardmäßig nur Heading 1
        self.document = Document(file_path)
    
    def extract_sections(self) -> List[Dict[str, List[str]]]:
        """Extrahiert Abschnitte basierend auf den definierten Überschriftsebenen."""
        sections = []
        current_section = {"title": "Start", "content": []}

        for para in self.document.paragraphs:
            # Prüfen, ob der Absatz eine der gewählten Überschriften ist
            if any(para.style.name.startswith(f"Heading {lvl}") for lvl in self.section_dividers):
                if current_section["content"]:  
                    sections.append(current_section)
                current_section = {"title": para.text.strip(), "content": []}
            else:
                if para.text.strip():
                    current_section["content"].append(para.text.strip())

        if current_section["content"]:
            sections.append(current_section)

        return sections
    
    def segment_text(self, text: str) -> List[str]:
        """Segmentiert Text in Sätze basierend auf Satzzeichen."""
        return re.split(r'(?<=[.!?])\s+|\n|\r', text)
    
    def extract_formatted_words(self, para) -> Tuple[str, Dict[int, Tuple[str, str]]]:
        """Erkennt fett oder unterstrichene Wörter und ersetzt sie durch Platzhalter."""
        formatted_words = {}
        new_text = []
        count = 0

        if not hasattr(para, "runs"):  # Falls bereits String, direkt zurückgeben
            return para, formatted_words

        for run in para.runs:
            for word in run.text.split():
                if run.bold or run.underline:
                    formatted_words[count] = (word, "bold" if run.bold else "underline")
                    new_text.append(f'##{count}##')
                else:
                    new_text.append(word)
                count += 1
        
        return " ".join(new_text), formatted_words
    
    def extract_segments(self) -> List[Dict[str, Union[List[str], Dict[int, Tuple[str, str]]]]]:
        """Extrahiert Segmente aus den Abschnitten."""
        sections = self.extract_sections()
        for section in sections:
            segmented_content = []
            formatted_data = {}
            for paragraph in section["content"]:
                processed_text, formats = self.extract_formatted_words(paragraph)
                segmented_sentences = self.segment_text(processed_text)
                formatted_data.update(formats)
                segmented_content.extend(segmented_sentences)
            section["content"] = segmented_content
            section["formats"] = formatted_data
        return sections
    
    def extract_xml_structure(self) -> ET.Element:
        """Erstellt eine XML-Kopie der DOCX-Struktur mit segmentierten Inhalten und Formatinfos."""
        root = ET.Element("document")
        
        for section in self.extract_segments():
            section_elem = ET.SubElement(root, "section", title=section["title"])
            for i, paragraph in enumerate(section["content"]):
                paragraph_elem = ET.SubElement(section_elem, "paragraph")
                paragraph_elem.text = paragraph
                
                # Falls Formatierungen vorhanden sind, speichern wir sie als XML-Attribut
                if section.get("formats") and i in section["formats"]:
                    format_info = section["formats"][i]
                    format_elem = ET.SubElement(paragraph_elem, "format", type=format_info[1])
                    format_elem.text = format_info[0]
        
        return root

if __name__ == "__main__":
    parser = DocxParser("example.docx", section_divider=1)  # Hier kann 1 oder 2 gesetzt werden
    print("\n--- Extracted Sections ---\n", parser.extract_sections())
    print("\n--- Extracted Segments ---\n", parser.extract_segments())
    xml_structure = parser.extract_xml_structure()
    print("\n--- XML Structure ---\n", ET.tostring(xml_structure, encoding='unicode'))
