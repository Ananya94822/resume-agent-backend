"""
Tool 1: Resume parser
Takes a raw PDF/DOCX/text resume and turns it into a clean structured
JSON object the rest of the agent's tools can reason over.
"""
import io
import pdfplumber
import docx
from app.llm_client import ask_llm_json
from app.tools.resume_cleaner import clean_resume_json

SYSTEM_PROMPT = """You are a resume-parsing engine. Extract structured data from raw
resume text. Be exhaustive with skills (include tools, languages, frameworks).
If a field is missing, use an empty string, empty list, or empty array as appropriate.

Return JSON in exactly this shape:
{
  "name": "", "email": "", "phone": "", "linkedin": "", "github": "",
  "summary": "",
  "skills": ["..."],
  "education": [{"degree": "", "institution": "", "year": "", "cgpa_or_percentage": ""}],
  "experience": [{"title": "", "company": "", "duration": "", "bullets": ["..."]}],
  "projects": [{"name": "", "description": "", "tech_used": ["..."], "bullets": ["..."]}],
  "certifications": ["..."]
}"""


def extract_text_from_bytes(file_bytes: bytes, filename: str) -> str:
    lower = filename.lower()
    if lower.endswith(".pdf"):
        text = []
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        return "\n".join(text)
    elif lower.endswith(".docx"):
        document = docx.Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in document.paragraphs)
    elif lower.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")
    else:
        raise ValueError("Unsupported file type. Please upload a PDF, DOCX, or TXT resume.")


def parse_resume(file_bytes: bytes, filename: str) -> dict:
    raw_text = extract_text_from_bytes(file_bytes, filename)
    if not raw_text.strip():
        raise ValueError("Could not extract any text from this file. It may be a scanned image.")
    structured = ask_llm_json(SYSTEM_PROMPT, f"Resume text:\n\n{raw_text}")
    structured = clean_resume_json(structured)
    structured["_raw_text"] = raw_text
    return structured
