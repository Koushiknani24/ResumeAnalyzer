"""Deterministic resume insights used alongside the optional Gemini workflow."""

from __future__ import annotations

import re
from collections import OrderedDict


SKILL_CATALOG = OrderedDict(
    {
        "Programming": ["Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Ruby", "PHP", "Kotlin", "Swift", "R"],
        "Frameworks": ["React", "Angular", "Vue", "Next.js", "Node.js", "Django", "Flask", "FastAPI", "Spring Boot", "Streamlit", "TensorFlow", "PyTorch"],
        "Databases": ["SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "Snowflake"],
        "Cloud & DevOps": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "CI/CD", "GitHub Actions", "Jenkins"],
        "AI & Data": ["Machine Learning", "Deep Learning", "NLP", "Generative AI", "LLM", "Data Analysis", "Pandas", "NumPy", "Scikit-learn", "Power BI", "Tableau"],
        "Tools": ["Git", "GitHub", "Jira", "Figma", "Linux", "Postman", "REST API", "GraphQL"],
        "Professional": ["Leadership", "Communication", "Agile", "Scrum", "Problem Solving", "Stakeholder Management"],
    }
)

SECTION_TERMS = {
    "Experience": ["experience", "employment", "work history", "internship"],
    "Education": ["education", "university", "college", "bachelor", "master", "degree"],
    "Projects": ["projects", "project experience", "portfolio"],
    "Certifications": ["certifications", "certificates", "certified"],
}


def _contains(text: str, term: str) -> bool:
    return bool(re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", text, re.IGNORECASE))


def extract_skill_categories(text: str) -> dict[str, list[str]]:
    """Return only catalogued skills explicitly present in the supplied text."""
    return {category: [skill for skill in skills if _contains(text, skill)] for category, skills in SKILL_CATALOG.items() if any(_contains(text, skill) for skill in skills)}


def flatten_skills(categories: dict[str, list[str]]) -> list[str]:
    return [skill for skills in categories.values() for skill in skills]


def find_sections(text: str) -> list[str]:
    return [name for name, terms in SECTION_TERMS.items() if any(_contains(text, term) for term in terms)]


def build_resume_insights(resume_text: str, job_description: str = "") -> dict:
    """Build transparent rule-based findings without using an LLM or inferred claims."""
    categories = extract_skill_categories(resume_text)
    resume_skills = flatten_skills(categories)
    sections = find_sections(resume_text)
    missing_sections = [section for section in SECTION_TERMS if section not in sections]
    insights = {"skill_categories": categories, "skills": resume_skills, "sections_found": sections, "missing_sections": missing_sections, "strengths": [], "improvements": [], "job_match": None}
    if resume_skills:
        insights["strengths"].append(f"Explicitly lists {len(resume_skills)} catalogued technical or professional skills.")
    if "Projects" in sections:
        insights["strengths"].append("Includes a projects or portfolio section.")
    if "Experience" in sections:
        insights["strengths"].append("Includes an experience-related section.")
    for section in missing_sections:
        insights["improvements"].append(f"Consider adding a clearly labeled {section} section if it is relevant to your background.")
    if job_description.strip():
        job_skills = flatten_skills(extract_skill_categories(job_description))
        resume_lookup = {skill.casefold() for skill in resume_skills}
        matching = [skill for skill in job_skills if skill.casefold() in resume_lookup]
        missing = [skill for skill in job_skills if skill.casefold() not in resume_lookup]
        coverage = round((len(matching) / len(job_skills)) * 100) if job_skills else None
        insights["job_match"] = {"required_skills_detected": job_skills, "matching_skills": matching, "missing_skills": missing, "coverage": coverage}
    return insights


def gap_recommendation(skill: str) -> str:
    return f"Build a small, documented project using {skill} and add a results-focused bullet when you can demonstrate it."
