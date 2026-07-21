"""
Tool 5: Resume tailoring
Rewrites an existing structured resume so it's optimized for a specific
job description — reordering/emphasizing relevant skills, rewriting
bullets to mirror the JD's language (for ATS keyword matching), and
never fabricating experience the student doesn't have.
"""
from app.llm_client import ask_llm_json

SYSTEM_PROMPT = """You are an expert resume writer for students applying to campus
placements. You will be given a student's existing structured resume (JSON) and a
job description analysis (JSON). Rewrite the resume to be ATS-optimized for this
specific role.

Hard rules:
- NEVER invent skills, experience, projects, or metrics the student doesn't have.
- You MAY rephrase existing bullets using the job description's terminology
  (e.g. "built REST APIs" -> "developed RESTful APIs" if the JD says "RESTful").
- You MAY reorder the skills list to put JD-relevant skills first.
- Every bullet should start with a strong action verb and, where the original
  data supports it, quantify impact.
- If the student is missing a required skill entirely, do not fabricate it —
  that's what the gap-analysis feature is for.

Return the SAME JSON shape as the input resume (name, email, phone, linkedin,
github, summary, skills, education, experience, projects, certifications), with
an added top-level field "tailoring_notes": ["short explanation of each notable change"]."""


def tailor_resume(resume_json: dict, jd_analysis: dict) -> dict:
    resume_for_prompt = {k: v for k, v in resume_json.items() if k != "_raw_text"}
    user_prompt = (
        f"Student's current resume:\n{resume_for_prompt}\n\n"
        f"Target job description analysis:\n{jd_analysis}"
    )
    return ask_llm_json(SYSTEM_PROMPT, user_prompt, max_tokens=3000)
