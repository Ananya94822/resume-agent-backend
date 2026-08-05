"""
Tool 5: Resume tailoring
Rewrites an existing structured resume so its optimized for a specific
job description -- reordering/emphasizing relevant skills, rewriting
bullets to mirror the JDs language (for ATS keyword matching), and
never fabricating experience the student doesnt have.
"""
from app.llm_client import ask_llm_json
from app.tools.resume_cleaner import clean_resume_json

SYSTEM_PROMPT = """You are an expert resume writer for students applying to campus
placements. You will be given a students existing structured resume (JSON), a
job description analysis (JSON), and a list of skills the student is genuinely
missing (already checked against synonyms/related tech, so treat this list as
accurate real gaps). Rewrite the resume to be ATS-optimized for this specific role.

Hard rules:
- NEVER invent skills, experience, projects, or metrics the student doesnt have.
- You MAY rephrase existing bullets using the job descriptions terminology
  (e.g. "built REST APIs" -> "developed RESTful APIs" if the JD says "RESTful").
- You MAY reorder the skills list to put JD-relevant skills first.
- Every bullet should start with a strong action verb and, where the original
  data supports it, quantify impact.
- If the "genuinely missing skills" list is non-empty, add a new field to your
  output called "currently_building" containing up to 5 of those skill names
  (comma-clean strings, no elaboration). This will be rendered on the resume as
  a short "Currently Building Skills In" line -- it must ONLY contain skills
  from the provided missing-skills list. Do not add a skill there that already
  appears (or has a synonym/related technology) in the students existing
  Skills section.
- If the missing-skills list is empty, return "currently_building": [].

Return the SAME JSON shape as the input resume (name, email, phone, linkedin,
github, summary, skills, education, experience, projects, certifications), plus
"currently_building" (list of strings) and "tailoring_notes" (list of short
explanations of each notable change)."""


def tailor_resume(resume_json: dict, jd_analysis: dict, missing_skills: list = None) -> dict:
    resume_for_prompt = {k: v for k, v in resume_json.items() if k != "_raw_text"}
    missing_skills = missing_skills or []
    user_prompt = (
        f"Students current resume:\n{resume_for_prompt}\n\n"
        f"Target job description analysis:\n{jd_analysis}\n\n"
        f"Genuinely missing skills (already checked against synonyms -- treat as "
        f"accurate, real gaps, not skills the student already has under another "
        f"name):\n{missing_skills}"
    )
    result = ask_llm_json(SYSTEM_PROMPT, user_prompt, max_tokens=3000)
    notes = result.pop("tailoring_notes", [])
    currently_building = result.pop("currently_building", [])
    result = clean_resume_json(result)
    result["tailoring_notes"] = notes
    result["currently_building"] = currently_building
    return result
