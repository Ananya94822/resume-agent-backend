"""
Skill matching with synonym/relation awareness.

Problem this fixes: a gap-analysis that trusts the LLM to compare skills
can still miss that "Relational databases" is already satisfied by
MySQL, PostgreSQL, or Django in the resume. This module is a deterministic
safety net applied AFTER the AIs answer, catching false gaps it missed.
"""

import re

SKILL_SYNONYMS = {
    "relational databases": {"sql", "mysql", "postgresql", "postgres", "oracle",
                              "sqlite", "mssql", "sql server", "django orm",
                              "database design", "dbms"},
    "sql": {"mysql", "postgresql", "postgres", "oracle", "sqlite", "mssql",
            "sql server", "relational databases", "dbms"},
    "nosql": {"mongodb", "dynamodb", "firebase", "cassandra", "redis"},
    "cloud platforms": {"aws", "azure", "gcp", "google cloud", "cloud computing"},
    "version control": {"git", "github", "gitlab", "bitbucket"},
    "containerization": {"docker", "kubernetes", "k8s", "podman"},
    "frontend framework": {"react", "vue", "angular", "svelte"},
    "backend framework": {"django", "flask", "fastapi", "express", "spring",
                           "spring boot", "node.js", "nodejs"},
    "rest apis": {"rest api", "restful api", "rest api design", "api development"},
    "data analysis": {"pandas", "numpy", "excel", "power bi", "tableau",
                       "data visualization"},
    "machine learning": {"ml", "scikit-learn", "sklearn", "tensorflow",
                          "pytorch", "nlp", "llm applications"},
    "ci/cd pipelines": {"ci/cd", "jenkins", "github actions", "gitlab ci",
                         "continuous integration", "continuous deployment"},
}


def _normalize(skill: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", skill.lower().strip())


def skill_is_covered(required_skill: str, resume_skills: list) -> bool:
    required_norm = _normalize(required_skill)
    resume_norm = {_normalize(s) for s in resume_skills}

    for rs in resume_norm:
        if not rs:
            continue
        if required_norm == rs or required_norm in rs or rs in required_norm:
            return True

    related = SKILL_SYNONYMS.get(required_norm, set())
    if related & resume_norm:
        return True

    for key, synonyms in SKILL_SYNONYMS.items():
        if required_norm in synonyms and key in resume_norm:
            return True

    return False
