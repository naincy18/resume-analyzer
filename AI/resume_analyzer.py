
from AI.skill_extractor import extract_skills, extract_experience
from AI.job_matcher import match_skills
from AI.semantic_matcher import calculate_similarity


def calculate_experience_score(resume_years, required_years):

    if resume_years is None or required_years is None:
        return None

    if resume_years < 0 or required_years < 0:
        raise ValueError("Experience years cannot be negative.")

    if required_years == 0:
        return 100.0

    score = min(resume_years / required_years, 1) * 100

    return round(score, 2)


def calculate_final_score(
    skill_score,
    semantic_score,
    experience_score
):
    # Define component weights
    weights = {
        "skill": 0.60,
        "semantic": 0.30,
        "experience": 0.10
    }

    scores = {
        "skill": skill_score,
        "semantic": semantic_score,
        "experience": experience_score
    }

    weighted_total = 0
    available_weight = 0

    for component, score in scores.items():

        if score is None:
            continue

        # Keep every component within 0–100
        bounded_score = max(0, min(float(score), 100))

        weighted_total += bounded_score * weights[component]
        available_weight += weights[component]

    if available_weight == 0:
        return None

    final_score = weighted_total / available_weight

    return round(final_score, 2)


def analyze_resume(resume_text, job_description):

    # Validate resume input
    if not isinstance(resume_text, str):
        raise ValueError("Resume text must be a string.")

    if not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    # Validate job description input
    if not isinstance(job_description, str):
        raise ValueError("Job description must be a string.")

    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    skill_result = match_skills(resume_skills, job_skills)
    skill_score = skill_result["match_score"]

    semantic_score = calculate_similarity(
        resume_text, job_description
    )

    resume_years = extract_experience(resume_text)
    required_years = extract_experience(job_description)

    experience_score = calculate_experience_score(
        resume_years, required_years
    )

    final_score = calculate_final_score(
        skill_score,
        semantic_score,
        experience_score
    )

    suggestions = []

    if skill_result["missing_skills"]:
        suggestions.append(
            "Consider developing these missing skills: "
            + ", ".join(skill_result["missing_skills"])
        )

    if skill_score is None:
        suggestions.append(
            "No recognized job skills were found. "
            "Review the job description or expand the skill vocabulary."
        )

    if resume_years is None:
        suggestions.append(
            "Add your years of relevant professional experience "
            "to your resume, if applicable."
        )

    elif required_years is not None and resume_years < required_years:
        suggestions.append(
            f"The job asks for {required_years:g} years of experience, "
            f"while your resume states {resume_years:g} years."
        )

    if not suggestions:
        suggestions.append(
            "Your resume covers the listed job skills well. "
            "Keep your experience and project descriptions specific."
        )

    return {
        "match_score": final_score,
        "skill_match_score": skill_score,
        "semantic_similarity": semantic_score,
        "experience_score": experience_score,
        "resume_experience": resume_years,
        "required_experience": required_years,
        "matched_skills": skill_result["matched_skills"],
        "missing_skills": skill_result["missing_skills"],
        "suggestions": suggestions
    }


resume_text = """
I am a software developer with 3 years of experience.
I have worked with Python, SQL, Machine Learning,
Data Analysis, Pandas and Git.
"""

job_description = """
We are looking for a developer with 2 years of experience.
Required skills include Python, SQL, FastAPI,
Machine Learning and Docker.
"""


if __name__ == "__main__":

    print("\nStarting Resume Analysis...")

    try:
        result = analyze_resume(resume_text, job_description)

        print("\n========== RESUME ANALYSIS REPORT ==========")
        print("Final Match Score:", result["match_score"])
        print("Skill Match Score:", result["skill_match_score"])
        print("Semantic Similarity:", result["semantic_similarity"])
        print("Resume Experience:", result["resume_experience"])
        print("Required Experience:", result["required_experience"])
        print("Experience Score:", result["experience_score"])

        print("\nMatched Skills:")
        print(result["matched_skills"])

        print("\nMissing Skills:")
        print(result["missing_skills"])

        print("\nSuggestions:")
        for suggestion in result["suggestions"]:
            print("-", suggestion)

    except ValueError as error:
        print("Input Error:", error)
