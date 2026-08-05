"""
Tool 4: Learning resource lookup.

IMPORTANT: never invent specific course URLs (hallucinated links break
trust). This module ships a curated map of stable, well-known resources
for common skills, and falls back to naming reputable platforms (without
a fabricated URL) for anything not in the map. Swap
`search_learning_resources` for a real search API (SerpAPI, Google
Custom Search, Coursera's own API) when you're ready for live results.

Synonym matching: a JD might ask for "Relational databases" while the
curated map has entries under "sql" -- these mean the same practical
skill, so SKILL_SYNONYMS links related terms together before falling
back to "no resource found."
"""

CURATED_RESOURCES = {
    "python": [
        {"title": "Python for Everybody", "platform": "Coursera (University of Michigan)",
         "url": "https://www.coursera.org/specializations/python", "certification": "Yes, shareable certificate"},
        {"title": "CS50s Introduction to Programming with Python", "platform": "edX / Harvard",
         "url": "https://www.edx.org/cs50", "certification": "Yes"},
    ],
    "sql": [
        {"title": "SQL for Data Science", "platform": "Coursera (UC Davis)",
         "url": "https://www.coursera.org/learn/sql-for-data-science", "certification": "Yes"},
    ],
    "react": [
        {"title": "React - The Complete Guide", "platform": "Udemy",
         "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/", "certification": "Yes"},
        {"title": "React official docs and tutorial", "platform": "react.dev",
         "url": "https://react.dev/learn", "certification": "No"},
    ],
    "data structures and algorithms": [
        {"title": "Data Structures and Algorithms Specialization", "platform": "Coursera (UC San Diego)",
         "url": "https://www.coursera.org/specializations/data-structures-algorithms", "certification": "Yes"},
    ],
    "machine learning": [
        {"title": "Machine Learning Specialization", "platform": "Coursera (Andrew Ng / DeepLearning.AI)",
         "url": "https://www.coursera.org/specializations/machine-learning-introduction", "certification": "Yes"},
    ],
    "aws": [
        {"title": "AWS Certified Cloud Practitioner", "platform": "AWS Skill Builder",
         "url": "https://skillbuilder.aws/", "certification": "Yes, official AWS certification"},
    ],
    "git": [
        {"title": "Git and GitHub for Beginners", "platform": "freeCodeCamp",
         "url": "https://www.freecodecamp.org/news/git-and-github-for-beginners/", "certification": "No"},
    ],
    "docker": [
        {"title": "Docker for Beginners", "platform": "freeCodeCamp (YouTube)",
         "url": "https://www.freecodecamp.org/news/docker-for-beginners/", "certification": "No"},
        {"title": "Docker Certified Associate prep", "platform": "Docker docs",
         "url": "https://docs.docker.com/get-started/", "certification": "No, but official starting point"},
    ],
    "containerization": [
        {"title": "Docker for Beginners", "platform": "freeCodeCamp (YouTube)",
         "url": "https://www.freecodecamp.org/news/docker-for-beginners/", "certification": "No"},
    ],
    "kubernetes": [
        {"title": "Kubernetes for Beginners", "platform": "freeCodeCamp (YouTube)",
         "url": "https://www.freecodecamp.org/news/learn-kubernetes-in-under-3-hours/", "certification": "No"},
    ],
    "flask": [
        {"title": "Flask Tutorial", "platform": "freeCodeCamp (YouTube)",
         "url": "https://www.freecodecamp.org/news/how-to-build-a-web-app-using-flask/", "certification": "No"},
    ],
    "ci/cd pipelines": [
        {"title": "CI/CD Pipeline Tutorial with GitHub Actions", "platform": "freeCodeCamp",
         "url": "https://www.freecodecamp.org/news/learn-continuous-integration-continuous-deployment/", "certification": "No"},
    ],
    "cloud platforms": [
        {"title": "AWS Certified Cloud Practitioner", "platform": "AWS Skill Builder",
         "url": "https://skillbuilder.aws/", "certification": "Yes, official AWS certification"},
        {"title": "Google Cloud Digital Leader", "platform": "Google Cloud Skills Boost",
         "url": "https://www.cloudskillsboost.google/", "certification": "Yes, official Google certification"},
    ],
}

SKILL_SYNONYMS = {
    "relational databases": "sql",
    "relational database": "sql",
    "mysql": "sql",
    "postgresql": "sql",
    "postgres": "sql",
    "database management": "sql",
    "dbms": "sql",
    "containers": "containerization",
    "k8s": "kubernetes",
    "cloud computing": "cloud platforms",
    "cloud": "cloud platforms",
    "aws cloud": "aws",
    "continuous integration": "ci/cd pipelines",
    "continuous deployment": "ci/cd pipelines",
    "ci/cd": "ci/cd pipelines",
    "dsa": "data structures and algorithms",
    "data structures & algorithms": "data structures and algorithms",
    "ml": "machine learning",
    "version control": "git",
}


def search_learning_resources(skill: str) -> dict:
    """Tool function the agent calls. `skill` is a free-text skill name."""
    key = skill.strip().lower()

    if key in CURATED_RESOURCES:
        return {"skill": skill, "resources": CURATED_RESOURCES[key], "source": "curated"}

    if key in SKILL_SYNONYMS and SKILL_SYNONYMS[key] in CURATED_RESOURCES:
        mapped_key = SKILL_SYNONYMS[key]
        return {"skill": skill, "resources": CURATED_RESOURCES[mapped_key], "source": "curated_synonym"}

    for k, v in CURATED_RESOURCES.items():
        if k in key or key in k:
            return {"skill": skill, "resources": v, "source": "curated_fuzzy"}

    return {
        "skill": skill,
        "resources": [],
        "source": "none",
        "note": (f"No curated resource for '{skill}' yet. Recommend the student search "
                 f"'{skill} course' on Coursera, Udemy, or freeCodeCamp, or check for an "
                 f"official certification from the tool/vendor itself."),
    }
