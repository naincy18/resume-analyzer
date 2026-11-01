
from AI.job_matcher import match_skills
from AI.resume_analyzer import (
    calculate_experience_score,
    analyze_resume
)
from AI.skill_extractor import extract_skills, extract_experience


def test_skill_extraction():
    text = "I have experience in Python, SQL and Machine Learning."
    skills = extract_skills(text)

    assert "Python" in skills
    assert "SQL" in skills


def test_skill_matching():
    result = match_skills(
        ["Python", "SQL"],
        ["Python", "SQL", "FastAPI"]
    )

    assert result["match_score"] == 66.67
    assert "fastapi" in result["missing_skills"]


def test_experience_extraction():
    text = "I have 3 years of experience in software development."
    assert extract_experience(text) == 3.0


def test_experience_scoring():
    assert calculate_experience_score(3, 2) == 100
    assert calculate_experience_score(1, 2) == 50
    assert calculate_experience_score(0, 2) == 0
    assert calculate_experience_score(None, 2) is None


def test_complete_resume_analysis():
    resume = """
    Python developer with 3 years of experience.
    Skilled in Python, SQL, Machine Learning,
    FastAPI and Data Analysis.
    """

    job = """
    Looking for a Python developer with 2 years
    of experience. Required skills: Python, SQL,
    Machine Learning, Docker and FastAPI.
    """

    result = analyze_resume(resume, job)

    expected_keys = [
        "match_score",
        "skill_match_score",
        "semantic_similarity",
        "experience_score",
        "resume_experience",
        "required_experience",
        "matched_skills",
        "missing_skills",
        "suggestions"
    ]

    for key in expected_keys:
        assert key in result

    assert 0 <= result["match_score"] <= 100
    assert isinstance(result["matched_skills"], list)
    assert isinstance(result["missing_skills"], list)
    assert isinstance(result["suggestions"], list)


def test_no_matching_skills():
    result = match_skills(
        ["Python", "Java"],
        ["Docker", "FastAPI"]
    )

    assert result["match_score"] == 0
    assert result["matched_skills"] == []
    assert len(result["missing_skills"]) == 2


def test_empty_job_skills():
    result = match_skills(
        ["Python", "Java"],
        []
    )

    assert result["match_score"] == 0
    assert result["matched_skills"] == []
    assert result["missing_skills"] == []


def test_experience_more_than_required():
    score = calculate_experience_score(10, 2)

    assert score == 100
