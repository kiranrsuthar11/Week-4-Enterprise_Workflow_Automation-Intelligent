from io import BytesIO, StringIO
import pandas as pd
from pypdf import PdfReader
from docx import Document as DocxDocument

def extract_text(content: bytes, extension: str) -> str:
    if extension == ".txt":
        return content.decode("utf-8", errors="replace")
    if extension == ".csv":
        frame = pd.read_csv(BytesIO(content), dtype=str, keep_default_na=False)
        return frame.to_string(index=False)
    if extension == ".pdf":
        reader = PdfReader(BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if extension == ".docx":
        doc = DocxDocument(BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError("Unsupported file extension")
