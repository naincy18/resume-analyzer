import re


# A starter list of skills our AI will recognize.
# We can expand this list as the project develops.
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

    Args:
        text: Resume text or job description.

    Returns:
        A list of skills found in the text.
    """

    if not isinstance(text, str):
        return []

    found_skills = []

    for skill in SKILL_LIST:
        # Match the skill as a whole phrase, ignoring capitalization.
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills


# Test the extractor with example resume text.
if __name__ == "__main__":

    sample_resume = """
    I have experience in Python, SQL, and Machine Learning.
    I have used Pandas and Scikit-learn for Data Analysis.
    I also know Git and have good Communication Skills.
    """

    skills = extract_skills(sample_resume)

    print("Sample resume:")
    print(sample_resume)

    print("\nSkills detected:")
    print(skills)

    print("\nTotal skills found:", len(skills))