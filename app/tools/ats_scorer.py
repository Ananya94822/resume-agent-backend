"""
Tool 3: ATS scorer
Deterministic keyword matching (so scores are stable and explainable)
plus a Claude pass for formatting/readability issues that keyword
matching can't catch.
"""
import re
from app.llm_client import ask_llm_json

FORMAT_SYSTEM_PROMPT = """You are an ATS (Applicant Tracking System) formatting auditor.
Given raw resume text, flag formatting issues that break ATS parsers: tables, text boxes,
columns, images, non-standard section headers, missing contact info, inconsistent dates,
unusual fonts/symbols used as bullets. Return JSON:
{
  "formatting_issues": ["..."],
  "missing_sections": ["..."],
  "suggestions": ["..."]
}
If none found, return empty arrays."""


def _normalize(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9\+\#\.]+", text.lower()))


def score_ats(resume_raw_text: str, resume_skills: list[str], jd_keywords: list[str]) -> dict:
    # Match against BOTH the raw resume text and the parsed skills list,
    # so this still works even if the caller didn't pass _raw_text.
    combined_text = resume_raw_text + " " + " ".join(resume_skills)
    resume_tokens = _normalize(combined_text)
    matched, missing = [], []
    for kw in jd_keywords:
        kw_tokens = _normalize(kw)
        if kw_tokens & resume_tokens:
            matched.append(kw)
        else:
            missing.append(kw)

    keyword_score = round(100 * len(matched) / max(len(jd_keywords), 1))

    if resume_raw_text.strip():
        format_report = ask_llm_json(FORMAT_SYSTEM_PROMPT, resume_raw_text)
    else:
        # No raw text available (e.g. resume_json was hand-built, not parsed
        # from a file) — skip formatting analysis rather than guessing.
        format_report = {
            "formatting_issues": [],
            "missing_sections": [],
            "suggestions": ["Provide the original resume's _raw_text to enable formatting checks."],
        }

    format_penalty = min(30, 10 * len(format_report.get("formatting_issues", [])))
    overall_score = max(0, keyword_score - format_penalty)

    return {
        "overall_score": overall_score,
        "keyword_match_score": keyword_score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "formatting_issues": format_report.get("formatting_issues", []),
        "missing_sections": format_report.get("missing_sections", []),
        "suggestions": format_report.get("suggestions", []),
    }