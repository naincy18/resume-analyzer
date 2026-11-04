
from AI.resume_analyzer import analyze_resume


evaluation_cases = [
    {
        "name": "Strong Match",
        "expected": "Most required skills should match.",
        "resume": """
        Python developer with 3 years of experience.
        Skilled in Python, SQL, Machine Learning,
        FastAPI and Docker.
        """,
        "job": """
        Python developer with 2 years of experience.
        Required skills: Python, SQL, Machine Learning,
        FastAPI and Docker.
        """
    },
    {
        "name": "Partial Match",
        "expected": "Some required skills should be missing.",
        "resume": """
        Software developer with 1 year of experience.
        Skilled in Python, SQL and Data Analysis.
        """,
        "job": """
        Developer with 2 years of experience.
        Required skills: Python, SQL, FastAPI,
        Docker and Machine Learning.
        """
    },
    {
        "name": "Poor Match",
        "expected": "Most required technical skills should be missing.",
        "resume": """
        I have 2 years of experience in customer service.
        Skilled in Excel, Communication and Teamwork.
        """,
        "job": """
        Backend developer with 3 years of experience.
        Required skills: Python, Django, SQL,
        Docker and FastAPI.
        """
    },
    {
        "name": "Experience Gap",
        "expected": "Skills should match, but experience score should be lower.",
        "resume": """
        Python developer with 1 year of experience.
        Skilled in Python, SQL, FastAPI and Docker.
        """,
        "job": """
        Python developer with 5 years of experience.
        Required skills: Python, SQL, FastAPI and Docker.
        """
    },
    {
        "name": "Missing Experience Information",
        "expected": "Experience score should be unavailable.",
        "resume": """
        Python developer skilled in Python, SQL,
        Machine Learning and FastAPI.
        """,
        "job": """
        Developer required with Python, SQL,
        Machine Learning and FastAPI.
        """
    }
]


def run_evaluation():

    print("\n========== AI MODEL EVALUATION ==========")

    # Display total evaluation cases
    total_cases = len(evaluation_cases)
    print("Total Test Cases:", total_cases)

    for case in evaluation_cases:

        print("\n----------------------------------------")
        print("Test Case:", case["name"])
        print("Expected Behavior:", case["expected"])

        result = analyze_resume(
            case["resume"],
            case["job"]
        )

        print("\nFinal Match Score:", result["match_score"])
        print("Skill Match Score:", result["skill_match_score"])
        print("Semantic Similarity:", result["semantic_similarity"])
        print("Experience Score:", result["experience_score"])

        print("Matched Skills:", result["matched_skills"])
        print("Missing Skills:", result["missing_skills"])

        # Check whether the strong match scenario behaves as expected
        if case["name"] == "Strong Match":
            passed = (
                result["match_score"] >= 80
                and len(result["missing_skills"]) == 0
            )

            print("Evaluation Result:", "PASS" if passed else "FAIL")

        # Check whether the partial match scenario behaves as expected
        elif case["name"] == "Partial Match":
            passed = (
                result["skill_match_score"] > 0
                and result["skill_match_score"] < 100
                and len(result["matched_skills"]) > 0
                and len(result["missing_skills"]) > 0
            )

            print("Evaluation Result:", "PASS" if passed else "FAIL")

        # Check whether the poor match scenario behaves as expected
        elif case["name"] == "Poor Match":
            passed = (
                result["skill_match_score"] == 0
                and len(result["matched_skills"]) == 0
                and len(result["missing_skills"]) > 0
            )

            print("Evaluation Result:", "PASS" if passed else "FAIL")

        # Check whether the experience gap scenario behaves as expected
        elif case["name"] == "Experience Gap":
            passed = (
                result["experience_score"] is not None
                and result["experience_score"] < 50
                and result["skill_match_score"] == 100
            )

            print("Evaluation Result:", "PASS" if passed else "FAIL")

        print("Suggestions:")
        for suggestion in result["suggestions"]:
            print("-", suggestion)

    print("\n========== EVALUATION COMPLETED ==========")


if __name__ == "__main__":
    run_evaluation()



