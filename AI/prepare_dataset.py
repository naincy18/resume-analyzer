
import pandas as pd
from pathlib import Path

# Dataset location
data_path = Path("datasets/job_descriptions.csv")

# Output location
output_path = Path("datasets/cleaned_job_descriptions.csv")

print("Loading job description dataset...")

# Read only the columns needed for our project
columns_to_keep = [
    "Job Id",
    "Job Title",
    "Role",
    "Job Description",
    "skills",
    "Qualifications",
    "Experience"
]

df = pd.read_csv(data_path, usecols=columns_to_keep)

print("Original dataset:", df.shape)

# Remove duplicate job records
df = df.drop_duplicates(subset=["Job Id"])

# Remove records without job descriptions or skills
df = df.dropna(subset=["Job Description", "skills"])

# Remove empty descriptions and skills
df["Job Description"] = df["Job Description"].astype(str).str.strip()
df["skills"] = df["skills"].astype(str).str.strip()

df = df[
    (df["Job Description"] != "") &
    (df["skills"] != "")
]

# Select 5,000 records for initial experiments
df = df.sample(
    n=min(5000, len(df)),
    random_state=42
)

# Save cleaned dataset
df.to_csv(output_path, index=False)

print("\nDATA CLEANING COMPLETED!")
print("Cleaned dataset shape:", df.shape)
print("Saved to:", output_path)

print("\nSample cleaned records:")
print(df[["Job Title", "skills"]].head(5).to_string(index=False))
