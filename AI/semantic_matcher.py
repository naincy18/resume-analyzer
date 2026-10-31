

from sentence_transformers import SentenceTransformer, util


# Model will initially be empty
model = None


def get_model():
    """
    Load the AI model only when it is needed.
    Load it once and reuse it afterwards.
    """
    global model

    if model is None:
        print("Loading AI model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


def calculate_similarity(resume_text, job_description):
    """
    Calculate semantic similarity between a resume
    and a job description.
    """

    # Get the AI model
    ai_model = get_model()

    # Convert both texts into numerical embeddings
    resume_embedding = ai_model.encode(
        resume_text,
        convert_to_tensor=True
    )

    job_embedding = ai_model.encode(
        job_description,
        convert_to_tensor=True
    )

    # Calculate cosine similarity
    similarity = util.cos_sim(
        resume_embedding,
        job_embedding
    )

    # Convert result into percentage
    similarity_score = float(similarity.item()) * 100

    return round(similarity_score, 2)


# Run sample code only when this file is executed directly
if __name__ == "__main__":

    # Sample resume
    resume_text = """
    I am a software developer with experience in Python,
    SQL, Machine Learning, Pandas and Data Analysis.
    I have built applications and worked with Git.
    """

    # Sample job description
    job_description = """
    We are looking for a Python developer with experience
    in SQL, machine learning, data processing and software development.
    Knowledge of FastAPI and Docker is preferred.
    """

    # Calculate similarity
    score = calculate_similarity(
        resume_text,
        job_description
    )

    print("\nSEMANTIC SIMILARITY RESULTS")
    print("-------------------------------")
    print("Semantic Similarity:", score, "%")