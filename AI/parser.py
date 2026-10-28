import re
import pdfplumber
import docx
from io import BytesIO

SECTION_HEADINGS = {
    "summary": ["summary", "objective", "profile"],
    "skills": ["skills", "technical skills"],
    "experience": ["experience", "work experience", "internships"],
    "projects": ["projects", "personal projects"],
    "education": ["education", "academic background"],
}

def extract_text(file_bytes: bytes, filename: str) -> str:
    if filename.lower().endswith(".pdf"):
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif filename.lower().endswith(".docx"):
        d = docx.Document(BytesIO(file_bytes))
        text = "\n".join(p.text for p in d.paragraphs)
    else:
        raise ValueError("Unsupported file type")
    return re.sub(r"\n{3,}", "\n\n", text).strip()

def split_sections(text: str) -> dict:
    sections, current = {}, "other"
    for line in text.splitlines():
        key = line.strip().lower().rstrip(":")
        match = next((s for s, names in SECTION_HEADINGS.items() if key in names), None)
        if match:
            current = match
            sections.setdefault(current, [])
        else:
            sections.setdefault(current, []).append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}