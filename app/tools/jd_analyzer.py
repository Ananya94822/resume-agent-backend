"""
Tool 2: Job description analyzer
Extracts the role, required vs. preferred skills, and ATS keywords
from a pasted job description.
"""
from app.llm_client import ask_llm_json

SYSTEM_PROMPT = """You analyze job descriptions for a campus placement platform.
Extract exactly this JSON shape:
{
  "role_title": "",
  "seniority": "intern | entry-level | mid | senior",
  "required_skills": ["..."],
  "preferred_skills": ["..."],
  "ats_keywords": ["..."],
  "responsibilities_summary": "",
  "min_qualifications": ""
}
required_skills = must-have, explicitly stated as required.
preferred_skills = "nice to have", "bonus", "familiarity with".
ats_keywords = important nouns/phrases an ATS system would scan for
(tools, frameworks, methodologies, certifications), deduplicated."""


def analyze_job_description(jd_text: str) -> dict:
    if not jd_text.strip():
        raise ValueError("Job description text is empty.")
    return ask_llm_json(SYSTEM_PROMPT, f"Job description:\n\n{jd_text}")
