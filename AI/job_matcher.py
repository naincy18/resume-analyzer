
def match_skills(resume_skills, job_skills):
    # Convert skills to lowercase for comparison
    resume_set = {skill.lower() for skill in resume_skills}
    job_set = {skill.lower() for skill in job_skills}

    # Compare skills
    matched_skills = resume_set.intersection(job_set)
    missing_skills = job_set.difference(resume_set)

    # No recognized job skills means score is unavailable
    if not job_set:
        match_score = None
    else:
        match_score = (
            len(matched_skills) / len(job_set)
        ) * 100

    return {
        "match_score": (
            round(match_score, 2)
            if match_score is not None else None
        ),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills)
    }


if __name__ == "__main__":
    from AI.skill_extractor import extract_skills

    resume_text = """
    Python developer with experience in Python, SQL,
    Pandas, Machine Learning and Git.
    """

    job_description = """
    Developer required with Python, SQL,
    Machine Learning, FastAPI and Docker.
    """

    result = match_skills(
        extract_skills(resume_text),
        extract_skills(job_description)
    )

    print("\nSKILL MATCHING RESULTS")
    print("Match Score:", result["match_score"])
    print("Matched Skills:", result["matched_skills"])
    print("Missing Skills:", result["missing_skills"])
