"""
ResumeAgent: the orchestrator.
"""
from app.llm_client import ask_llm_json
from app.tools.resume_parser import parse_resume
from app.tools.jd_analyzer import analyze_job_description
from app.tools.ats_scorer import score_ats
from app.tools.resume_tailor import tailor_resume
from app.tools.resume_builder import build_resume_from_scratch
from app.tools.skill_resources import search_learning_resources
from app.tools.interview_prep import get_interview_prep

GAP_SYSTEM_PROMPT = """You are a career-readiness assistant for a college placement
platform. Compare a student's resume skills against a job's required and preferred
skills. Identify every required/preferred skill the student is missing.

Return JSON in exactly this shape:
{
  "gaps": [
    {"skill": "Docker", "type": "required", "why": "one short sentence on why it matters for this role"}
  ],
  "priority_order": ["skill name", "skill name"],
  "encouragement": "2-3 sentence encouraging note acknowledging their existing strengths"
}
Order "gaps" with required skills first, then preferred. "priority_order" should
list the 1-3 skills most worth learning first, by name, matching entries in "gaps".
If there are no gaps at all, return an empty "gaps" list and a congratulatory
encouragement note."""


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

    def gap_analysis(self, resume_json: dict, jd_analysis: dict) -> dict:
        user_prompt = (
            f"Student's current skills: {resume_json.get('skills', [])}\n\n"
            f"Target role: {jd_analysis.get('role_title')}\n"
            f"Required skills: {jd_analysis.get('required_skills', [])}\n"
            f"Preferred skills: {jd_analysis.get('preferred_skills', [])}"
        )
        result = ask_llm_json(GAP_SYSTEM_PROMPT, user_prompt, max_tokens=2000)

        for gap in result.get("gaps", []):
            lookup = search_learning_resources(gap.get("skill", ""))
            gap["resources"] = lookup.get("resources", [])
            gap["resource_note"] = lookup.get("note", "")

        return result

    def tailor_resume(self, resume_json: dict, jd_analysis: dict) -> dict:
        return tailor_resume(resume_json, jd_analysis)

    def build_resume(self, student_input: dict) -> dict:
        return build_resume_from_scratch(student_input)

    def interview_prep(self, resume_json: dict, jd_analysis: dict) -> dict:
        return get_interview_prep(resume_json, jd_analysis)


agent = ResumeAgent()
