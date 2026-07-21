"""
Tool 4: Learning resource lookup.

IMPORTANT: Claude should never invent specific course URLs (it can
hallucinate broken links). This module ships a curated map of stable,
well-known resources for common skills, and falls back to naming
reputable platforms (without a fabricated URL) for anything not in
the map. Swap `search_learning_resources` for a real search API
(SerpAPI, Google Custom Search, Coursera's own API) when you're ready
for live, always-current results.
"""

CURATED_RESOURCES = {
    "python": [
        {"title": "Python for Everybody", "platform": "Coursera (University of Michigan)",
         "url": "https://www.coursera.org/specializations/python", "certification": "Yes, shareable certificate"},
        {"title": "CS50's Introduction to Programming with Python", "platform": "edX / Harvard",
         "url": "https://www.edx.org/cs50", "certification": "Yes"},
    ],
    "sql": [
        {"title": "SQL for Data Science", "platform": "Coursera (UC Davis)",
         "url": "https://www.coursera.org/learn/sql-for-data-science", "certification": "Yes"},
    ],
    "react": [
        {"title": "React - The Complete Guide", "platform": "Udemy",
         "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/", "certification": "Yes"},
        {"title": "React official docs & tutorial", "platform": "react.dev",
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
}


def search_learning_resources(skill: str) -> dict:
    """Tool function the agent calls. `skill` is a free-text skill name."""
    key = skill.strip().lower()
    if key in CURATED_RESOURCES:
        return {"skill": skill, "resources": CURATED_RESOURCES[key], "source": "curated"}

    # Fuzzy fallback: partial match against curated keys
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
