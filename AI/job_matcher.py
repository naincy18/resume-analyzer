
from AI.skill_extractor import extract_skills


def match_skills(resume_skills, job_skills):
    # Convert skills to lowercase for comparison
    resume_set = {skill.lower() for skill in resume_skills}
    job_set = {skill.lower() for skill in job_skills}

    # Compare skills
    matched_skills = resume_set.intersection(job_set)
    missing_skills = job_set.difference(resume_set)

    # Calculate match percentage
    if not job_set:
        match_score = 0
    else:
        match_score = (len(matched_skills) / len(job_set)) * 100

    return {
        "match_score": round(match_score, 2),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills)
    }


# Run this sample only when this file is executed directly
if __name__ == "__main__":

    # Sample resume text
    resume_text = """
    I am a software developer with experience in Python,
    SQL, Pandas, Machine Learning and Git.

    I have also worked on data analysis projects.
    """

    # Sample job description
    job_description = """
    We are looking for a developer with Python,
    SQL, Machine Learning, FastAPI and Docker skills.
    """

    # Automatically extract skills from both texts
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    # Compare the extracted skills
    result = match_skills(resume_skills, job_skills)

    # Display results
    print("\nRESUME ANALYSIS RESULTS")
    print("----------------------------")

    print("Resume Skills:", resume_skills)
    print("Job Required Skills:", job_skills)

    print("\nMATCHING RESULTS")
    print("----------------------------")

    print("Match Score:", result["match_score"], "%")
    print("Matched Skills:", result["matched_skills"])
    print("Missing Skills:", result["missing_skills"])