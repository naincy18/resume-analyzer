def analyze_resume(resume_text: str, job_description: str) -> dict:
    """Temporary fake AI function for backend testing."""

    return {
        "match_score": 77.5,
        "matched_skills": ["Python", "SQL"],
        "missing_skills": ["FastAPI"],
        "semantic_similarity": 75,
        "suggestions": ["Add relevant FastAPI project experience"],
    }