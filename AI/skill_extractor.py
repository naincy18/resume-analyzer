
import re


# Skills our AI can recognize
SKILL_LIST = [
    "Python",
    "Java",
    "JavaScript",
    "C++",
    "SQL",
    "HTML",
    "CSS",
    "React",
    "Node.js",
    "FastAPI",
    "Django",
    "Flask",
    "Machine Learning",
    "Deep Learning",
    "Data Analysis",
    "Data Science",
    "Natural Language Processing",
    "NLP",
    "Artificial Intelligence",
    "Excel",
    "Power BI",
    "Tableau",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "TensorFlow",
    "PyTorch",
    "Git",
    "Docker",
    "AWS",
    "Communication",
    "Communication Skills",
    "Project Management",
    "Problem Solving",
    "Leadership",
    "Teamwork",
]


def extract_skills(text):
    """
    Find recognized skills in a piece of text.
    """

    if not isinstance(text, str):
        return []

    found_skills = []

    for skill in SKILL_LIST:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills


def extract_experience(text):
    """
    Extract the highest explicitly stated number of years
    of experience from text.

    Returns:
        Number of years, or None if no experience is found.
    """

    if not isinstance(text, str):
        return None

    pattern = (
        r"(\d+(?:\.\d+)?)\s*\+?\s*"
        r"(?:years?|yrs?)\s*"
        r"(?:of\s+)?"
        r"(?:relevant\s+)?"
        r"experience"
    )

    matches = re.findall(pattern, text, re.IGNORECASE)

    if not matches:
        return None

    years = [float(value) for value in matches]

    return max(years)


# Test the extractor
if __name__ == "__main__":

    sample_resume = """
    I am a software developer with 3 years of experience
    in Python, JavaScript, React, SQL and Docker.

    I have worked on several software development projects.
    """

    skills = extract_skills(sample_resume)
    experience = extract_experience(sample_resume)

    print("Sample resume:")
    print(sample_resume)

    print("\nSkills detected:")
    print(skills)

    print("\nTotal skills found:", len(skills))

    print("\nExperience detected:", experience, "years")