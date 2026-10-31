
from AI.skill_extractor import extract_skills, extract_experience
from AI.job_matcher import match_skills
from AI.semantic_matcher import calculate_similarity


def calculate_experience_score(resume_years, required_years):
    """
    Compare candidate experience with job requirements.
    """

    if resume_years is None or required_years is None:
        return None

    if required_years <= 0:
        return 100.0

    score = min(resume_years / required_years, 1) * 100

    return round(score, 2)


def analyze_resume(resume_text, job_description):

    # Extract skills
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    # Compare skills
    skill_result = match_skills(resume_skills, job_skills)
    skill_score = skill_result["match_score"]

    # Calculate semantic similarity
    semantic_score = calculate_similarity(
        resume_text,
        job_description
    )

    # Extract experience
    resume_years = extract_experience(resume_text)
    required_years = extract_experience(job_description)

    # Calculate experience relevance
    experience_score = calculate_experience_score(
        resume_years,
        required_years
    )

    # Use a neutral placeholder if experience is unavailable
    experience_score_for_total = (
        experience_score if experience_score is not None else 50
    )

    # Calculate final score
    final_score = (
        (0.60 * skill_score) +
        (0.30 * semantic_score) +
        (0.10 * experience_score_for_total)
    )

    # Generate suggestions
    suggestions = []

    if skill_result["missing_skills"]:
        suggestions.append(
            "Consider developing these missing skills: "
            + ", ".join(skill_result["missing_skills"])
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
        "match_score": round(final_score, 2),
        "skill_match_score": skill_score,
        "semantic_similarity": semantic_score,
        "experience_score": experience_score,
        "resume_experience": resume_years,
        "required_experience": required_years,
        "matched_skills": skill_result["matched_skills"],
        "missing_skills": skill_result["missing_skills"],
        "suggestions": suggestions
    }


# Sample resume
resume_text = """
I am a software developer with 3 years of experience.

I have worked with Python, SQL, Machine Learning,
Data Analysis, Pandas and Git.

I have built data analysis projects and software applications.
"""

# Sample job description
job_description = """
We are looking for a developer with 2 years of experience.

Required skills include Python, SQL, FastAPI,
Machine Learning and Docker.

The candidate should understand software development
and data analysis.
"""


if __name__ == "__main__":

    print("\nStarting Resume Analysis...")

    result = analyze_resume(resume_text, job_description)

    print("\n========== RESUME ANALYSIS REPORT ==========")

    print("\nFinal Match Score:", result["match_score"], "%")
    print("Skill Match Score:", result["skill_match_score"], "%")
    print("Semantic Similarity:", result["semantic_similarity"], "%")

    print("Resume Experience:", result["resume_experience"], "years")
    print("Required Experience:", result["required_experience"], "years")

    if result["experience_score"] is not None:
        print("Experience Score:", result["experience_score"], "%")
    else:
        print("Experience Score: Not available (using 50% placeholder in final score)")

    print("\nMatched Skills:")
    print(result["matched_skills"])

    print("\nMissing Skills:")
    print(result["missing_skills"])

    print("\nSuggestions:")
    for suggestion in result["suggestions"]:
        print("-", suggestion)

    print("\n============================================")