"""
ResumeAgent: the orchestrator.

Each public method is one capability your app calls. Internally, some
methods just call one tool; "gap_analysis" runs a real Claude tool-use
loop where the model decides, for each missing skill, whether it needs
to look up learning resources.
"""
from app.llm_client import ask_llm_with_tools
from app.tools.resume_parser import parse_resume
from app.tools.jd_analyzer import analyze_job_description
from app.tools.ats_scorer import score_ats
from app.tools.resume_tailor import tailor_resume
from app.tools.resume_builder import build_resume_from_scratch
from app.tools.skill_resources import search_learning_resources
from app.tools.interview_prep import get_interview_prep

GAP_SYSTEM_PROMPT = """You are a career-readiness assistant for a college placement
platform. You'll be given a student's resume skills and a target job description's
required + preferred skills. Identify which required/preferred skills the student is
missing. For EACH missing skill, call search_learning_resources to find how they can
learn it, then produce a final report as plain text with this structure:

## Skill gaps for this role
- **<skill>** (required/preferred): <1 line on why it matters for this role>
  - Resource: <platform - title - url if available>
  - Certification: <yes/no and name if available>

End with a short paragraph of overall encouragement and a suggested priority order
for closing the gaps (which 1-2 skills to focus on first)."""


class ResumeAgent:
    def parse_resume(self, file_bytes: bytes, filename: str) -> dict:
        return parse_resume(file_bytes, filename)

    def analyze_job(self, jd_text: str) -> dict:
        return analyze_job_description(jd_text)

    def ats_score(self, resume_json: dict, jd_analysis: dict) -> dict:
        return score_ats(
            resume_raw_text=resume_json.get("_raw_text", ""),
            resume_skills=resume_json.get("skills", []),
            jd_keywords=jd_analysis.get("ats_keywords", []),
        )

    def gap_analysis(self, resume_json: dict, jd_analysis: dict) -> str:
        user_prompt = (
            f"Student's current skills: {resume_json.get('skills', [])}\n\n"
            f"Target role: {jd_analysis.get('role_title')}\n"
            f"Required skills: {jd_analysis.get('required_skills', [])}\n"
            f"Preferred skills: {jd_analysis.get('preferred_skills', [])}"
        )
        return ask_llm_with_tools(
            system_prompt=GAP_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            tool_functions=[search_learning_resources],
            max_tokens=2000,
        )

    def tailor_resume(self, resume_json: dict, jd_analysis: dict) -> dict:
        return tailor_resume(resume_json, jd_analysis)

    def build_resume(self, student_input: dict) -> dict:
        return build_resume_from_scratch(student_input)


    def interview_prep(self, resume_json: dict, jd_analysis: dict) -> dict:
        return get_interview_prep(resume_json, jd_analysis)


agent = ResumeAgent()

