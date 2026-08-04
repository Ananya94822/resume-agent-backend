"""
Tool 8: Interview prep
Generates likely interview questions for a specific job, grounded in
both the job description and the student's own resume (so it can ask
about their actual projects, not generic ones).

Important: we do NOT claim a literal statistical probability (e.g. "80%
chance") since no verified dataset of real interviewer behavior exists.
Instead we use honest qualitative confidence tags based on how central
a topic is to the stated role.
"""
from app.llm_client import ask_llm_json

SYSTEM_PROMPT = """You are an experienced technical interviewer and campus
placement coach. Given a job description analysis and a candidate's resume,
generate realistic interview questions for THIS specific role and THIS
specific candidate.

Draw questions from four sources:
1. Required skills in the JD (core technical questions)
2. Preferred skills in the JD (bonus/stretch questions)
3. The candidate's OWN resume -- ask about their specific projects and
   experience by name, the way a real interviewer would
4. Common behavioral/HR questions appropriate for this seniority level

For each question, assign a confidence label -- ONLY one of these three,
never a percentage or invented statistic:
- "Very Likely": directly tests a required skill or is a near-universal
  question for this type of role
- "Likely": commonly asked for this seniority/role but not guaranteed
- "Possible": tests a preferred/bonus skill or is situational

Return JSON:
{
  "questions": [
    {"category": "Technical - Required Skills", "question": "...", "confidence": "Very Likely", "why": "one short sentence"},
    {"category": "Technical - Preferred Skills", "question": "...", "confidence": "Possible", "why": "..."},
    {"category": "About Your Projects", "question": "...", "confidence": "Very Likely", "why": "..."},
    {"category": "Behavioral", "question": "...", "confidence": "Likely", "why": "..."}
  ],
  "prep_tips": ["2-3 short, practical tips for preparing for this specific interview"]
}
Generate 10-14 questions total across all categories, weighted toward
required skills and the candidate's own projects."""


def get_interview_prep(resume_json: dict, jd_analysis: dict) -> dict:
    resume_summary = {
        "skills": resume_json.get("skills", []),
        "experience": resume_json.get("experience", []),
        "projects": resume_json.get("projects", []),
    }
    user_prompt = (
        f"Job description analysis:\n{jd_analysis}\n\n"
        f"Candidate's resume (skills, experience, projects):\n{resume_summary}"
    )
    return ask_llm_json(SYSTEM_PROMPT, user_prompt, max_tokens=3000)
