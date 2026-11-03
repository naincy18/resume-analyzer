
import pytest

from AI.job_matcher import match_skills
from AI.resume_analyzer import (
    calculate_experience_score,
    calculate_final_score,
    analyze_resume
)
from AI.skill_extractor import extract_skills, extract_experience


# 1. Skill extraction tests

def test_skill_extraction():
    text = "I have experience in Python, SQL and Machine Learning."
    skills = extract_skills(text)

    assert "Python" in skills
    assert "SQL" in skills


def test_resume_without_recognized_skills():
    resume_skills = extract_skills(
        "I am a hardworking and motivated professional."
    )

    assert resume_skills == []


def test_job_without_recognized_skills():
    job_skills = extract_skills(
        "We need a motivated person for our organization."
    )

    assert job_skills == []


# 2. Skill matching tests

def test_skill_matching():
    result = match_skills(
        ["Python", "SQL"],
        ["Python", "SQL", "FastAPI"]
    )

    assert result["match_score"] == 66.67
    assert "fastapi" in result["missing_skills"]


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

    assert result["match_score"] is None
    assert result["matched_skills"] == []
    assert result["missing_skills"] == []


def test_empty_resume_skills():
    result = match_skills(
        [],
        ["Python", "SQL"]
    )

    assert result["match_score"] == 0
    assert result["matched_skills"] == []
    assert len(result["missing_skills"]) == 2


# 3. Experience extraction tests

def test_experience_extraction():
    text = "I have 3 years of experience in software development."

    assert extract_experience(text) == 3.0


def test_experience_not_mentioned():
    text = "I am a Python developer with strong technical skills."

    assert extract_experience(text) is None


# 4. Experience scoring tests

def test_experience_scoring():
    assert calculate_experience_score(3, 2) == 100
    assert calculate_experience_score(1, 2) == 50
    assert calculate_experience_score(0, 2) == 0
    assert calculate_experience_score(None, 2) is None


def test_experience_more_than_required():
    score = calculate_experience_score(10, 2)

    assert score == 100


def test_zero_required_experience():
    score = calculate_experience_score(3, 0)

    assert score == 100.0


def test_negative_required_experience():
    with pytest.raises(
        ValueError,
        match="Experience years cannot be negative."
    ):
        calculate_experience_score(3, -2)


def test_negative_resume_experience():
    with pytest.raises(
        ValueError,
        match="Experience years cannot be negative."
    ):
        calculate_experience_score(-1, 2)


# 5. Complete resume analysis tests

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


def test_missing_experience_in_both_documents():
    resume = "Python developer skilled in SQL and Django."

    job = "Looking for a Python developer skilled in SQL and Django."

    result = analyze_resume(resume, job)

    assert result["resume_experience"] is None
    assert result["required_experience"] is None
    assert result["experience_score"] is None

    assert any(
        "experience" in suggestion.lower()
        for suggestion in result["suggestions"]
    )


def test_resume_experience_below_requirement():
    resume = """
    Python developer with 1 year of experience.
    Skilled in Python and SQL.
    """

    job = """
    Python developer with 3 years of experience.
    Required skills include Python and SQL.
    """

    result = analyze_resume(resume, job)

    assert result["resume_experience"] == 1.0
    assert result["required_experience"] == 3.0
    assert result["experience_score"] == 33.33

    assert any(
        "job asks for" in suggestion.lower()
        for suggestion in result["suggestions"]
    )


# 6. Input validation tests

def test_empty_resume_text():
    with pytest.raises(
        ValueError,
        match="Resume text cannot be empty."
    ):
        analyze_resume("", "Python developer required")


def test_empty_job_description():
    with pytest.raises(
        ValueError,
        match="Job description cannot be empty."
    ):
        analyze_resume("Python developer with experience", "")


def test_resume_with_only_spaces():
    with pytest.raises(
        ValueError,
        match="Resume text cannot be empty."
    ):
        analyze_resume("    ", "Python developer required")


def test_job_description_with_only_spaces():
    with pytest.raises(
        ValueError,
        match="Job description cannot be empty."
    ):
        analyze_resume("Python developer with experience", "    ")


def test_none_resume_text():
    with pytest.raises(
        ValueError,
        match="Resume text cannot be empty."
    ):
        analyze_resume(None, "Python developer required")


def test_none_job_description():
    with pytest.raises(
        ValueError,
        match="Job description cannot be empty."
    ):
        analyze_resume("Python developer with experience", None)


# 7. Final score calculation tests

def test_final_score_with_all_components():
    score = calculate_final_score(80, 70, 100)

    assert score == 79.0


def test_final_score_without_experience():
    score = calculate_final_score(80, 70, None)

    assert score == 76.67


def test_final_score_without_skills():
    score = calculate_final_score(None, 80, 100)

    assert score == 85.0


def test_final_score_all_components_missing():
    score = calculate_final_score(None, None, None)

    assert score is None


def test_final_score_never_exceeds_100():
    score = calculate_final_score(120, 110, 105)

    assert score == 100.0
