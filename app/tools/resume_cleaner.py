"""
Shared cleanup applied to every resume JSON before it is returned from the
API -- whether from parsing, building, or tailoring. Models sometimes write
placeholder text like "Not Specified" or "N/A" instead of leaving a field
empty despite being told not to; this scrubs that out.
"""

_JUNK_VALUES = {"not specified", "n/a", "na", "tbd", "unknown", "none", "-", ""}


def _scrub(value):
    if isinstance(value, str):
        return "" if value.strip().lower() in _JUNK_VALUES else value.strip()
    return value


def clean_resume_json(data: dict) -> dict:
    if not isinstance(data, dict):
        return data

    cleaned = dict(data)
    for key in ("name", "email", "phone", "linkedin", "github", "summary"):
        if key in cleaned:
            cleaned[key] = _scrub(cleaned[key])

    if cleaned.get("skills"):
        cleaned["skills"] = [_scrub(s) for s in cleaned["skills"] if _scrub(s)]

    if cleaned.get("certifications"):
        cleaned["certifications"] = [_scrub(c) for c in cleaned["certifications"] if _scrub(c)]

    if cleaned.get("education"):
        scrubbed_edu = []
        for ed in cleaned["education"]:
            ed = {k: _scrub(v) for k, v in ed.items()}
            if ed.get("degree") or ed.get("institution"):
                scrubbed_edu.append(ed)
        cleaned["education"] = scrubbed_edu

    if cleaned.get("experience"):
        scrubbed_exp = []
        for exp in cleaned["experience"]:
            exp = dict(exp)
            for k in ("title", "company", "duration"):
                if k in exp:
                    exp[k] = _scrub(exp[k])
            if exp.get("bullets"):
                exp["bullets"] = [_scrub(b) for b in exp["bullets"] if _scrub(b)]
            if exp.get("title") or exp.get("company"):
                scrubbed_exp.append(exp)
        cleaned["experience"] = scrubbed_exp

    if cleaned.get("projects"):
        scrubbed_proj = []
        for proj in cleaned["projects"]:
            proj = dict(proj)
            for k in ("name", "description"):
                if k in proj:
                    proj[k] = _scrub(proj[k])
            if proj.get("tech_used"):
                proj["tech_used"] = [_scrub(t) for t in proj["tech_used"] if _scrub(t)]
            if proj.get("bullets"):
                proj["bullets"] = [_scrub(b) for b in proj["bullets"] if _scrub(b)]
            if proj.get("name"):
                scrubbed_proj.append(proj)
        cleaned["projects"] = scrubbed_proj

    return cleaned
