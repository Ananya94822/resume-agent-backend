"""
Tool 6: Resume builder (from scratch)
Takes a simple form of basic student info and produces a full,
ATS-friendly structured resume -- optionally already tailored toward
a target role if one is given.
"""
from app.llm_client import ask_llm_json
from app.tools.resume_cleaner import clean_resume_json

SYSTEM_PROMPT = """You are an expert resume writer helping a student who has no
resume yet. You'll receive basic raw input: education, skills they know, projects
or internships they've done (even informally described), and optionally a target
role. Turn this into a polished, ATS-friendly resume.

Rules:
- Write 2-4 strong bullet points per project/experience, each starting with an
  action verb, based ONLY on what the student described. Elaborate on phrasing
  and structure, but do not invent facts, tools, or outcomes not mentioned.
- If the student gives very little detail for a project, ask yourself what a
  student who did that project would plausibly and safely also have done
  (e.g. "used Git for version control" for any coding project) - only include
  such reasonable, low-risk inferences, and mark them in "inferred_bullets".
- Write a 2-3 sentence professional summary tailored to the target role if given.
- Order skills with the most relevant to the target role first.

Return JSON:
{
  "name": "", "email": "", "phone": "", "linkedin": "", "github": "",
  "summary": "",
  "skills": ["..."],
  "education": [{"degree": "", "institution": "", "year": "", "cgpa_or_percentage": ""}],
  "experience": [{"title": "", "company": "", "duration": "", "bullets": ["..."]}],
  "projects": [{"name": "", "description": "", "tech_used": ["..."], "bullets": ["..."]}],
  "certifications": ["..."],
  "inferred_bullets": ["list any bullet text you added that wasn't explicitly stated"]
}"""


def build_resume_from_scratch(student_input: dict) -> dict:
    result = ask_llm_json(SYSTEM_PROMPT, f"Student input:\n{student_input}", max_tokens=3000)
    inferred = result.pop("inferred_bullets", [])
    result = clean_resume_json(result)
    result["inferred_bullets"] = inferred
    return result
