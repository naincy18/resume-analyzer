
from pathlib import Path
from datetime import datetime
from time import perf_counter

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
    },
    {
        "name": "No Matching Skills",
        "expected": "No required job skills should match the resume.",
        "resume": """
        I have 2 years of experience in customer service.
        Skilled in Excel, Communication and Teamwork.
        """,
        "job": """
        Software developer with 2 years of experience.
        Required skills: Python, Django, SQL,
        Docker and FastAPI.
        """
    },
    {
        "name": "Empty Resume",
        "expected": "Analyzer should reject an empty resume.",
        "resume": "",
        "job": """
        Python developer required with Python, SQL and FastAPI.
        """
    }
]


def run_evaluation():

    start_time = perf_counter()

    report = []

    def log(message=""):
        print(message)
        report.append(str(message))

    log("\n========== AI MODEL EVALUATION ==========")

    evaluation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log("Evaluation Date and Time: " + evaluation_time)

    total_cases = len(evaluation_cases)
    passed_cases = 0
    failed_cases = 0

    log("Total Test Cases: " + str(total_cases))

    for case in evaluation_cases:

        log("\n----------------------------------------")
        log("Test Case: " + case["name"])
        log("Expected Behavior: " + case["expected"])

        if case["name"] == "Empty Resume":

            try:
                analyze_resume(case["resume"], case["job"])
                passed = False

            except ValueError as error:
                passed = str(error) == "Resume text cannot be empty."
                log("Validation Message: " + str(error))

        else:

            result = analyze_resume(
                case["resume"],
                case["job"]
            )

            log("\nFinal Match Score: " + str(result["match_score"]))
            log("Skill Match Score: " + str(result["skill_match_score"]))
            log("Semantic Similarity: " + str(result["semantic_similarity"]))
            log("Experience Score: " + str(result["experience_score"]))

            log("Matched Skills: " + str(result["matched_skills"]))
            log("Missing Skills: " + str(result["missing_skills"]))

            if case["name"] == "Strong Match":
                passed = (
                    result["match_score"] >= 80
                    and len(result["missing_skills"]) == 0
                )

            elif case["name"] == "Partial Match":
                passed = (
                    result["skill_match_score"] > 0
                    and result["skill_match_score"] < 100
                    and len(result["matched_skills"]) > 0
                    and len(result["missing_skills"]) > 0
                )

            elif case["name"] == "Poor Match":
                passed = (
                    result["skill_match_score"] == 0
                    and len(result["matched_skills"]) == 0
                    and len(result["missing_skills"]) > 0
                )

            elif case["name"] == "Experience Gap":
                passed = (
                    result["experience_score"] is not None
                    and result["experience_score"] < 50
                    and result["skill_match_score"] == 100
                )

            elif case["name"] == "Missing Experience Information":
                passed = (
                    result["experience_score"] is None
                    and result["match_score"] is not None
                )

            elif case["name"] == "No Matching Skills":
                passed = (
                    result["skill_match_score"] == 0
                    and len(result["matched_skills"]) == 0
                    and len(result["missing_skills"]) > 0
                )

            log("Suggestions:")
            for suggestion in result["suggestions"]:
                log("- " + suggestion)

        if passed:
            passed_cases += 1
        else:
            failed_cases += 1

        log("Evaluation Result: " + ("PASS" if passed else "FAIL"))

    evaluation_duration = perf_counter() - start_time

    log("\n========== EVALUATION SUMMARY ==========")
    log("Total Test Cases: " + str(total_cases))
    log("Passed: " + str(passed_cases))
    log("Failed: " + str(failed_cases))

    pass_percentage = (
        (passed_cases / total_cases) * 100
        if total_cases > 0 else 0
    )

    log("Pass Percentage: " + str(round(pass_percentage, 2)) + "%")

    overall_result = "PASS" if failed_cases == 0 else "FAIL"
    log("Overall Result: " + overall_result)

    log("Evaluation Duration: " + str(round(evaluation_duration, 2)) + " seconds")

    log("\n========== EVALUATION COMPLETED ==========")

    report_path = Path(__file__).with_name("evaluation_report.txt")

    report_path.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    print("\nEvaluation report saved to:", report_path)


if __name__ == "__main__":
    run_evaluation()
