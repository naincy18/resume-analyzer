
import pandas as pd
from pathlib import Path

# Locate the dataset
file_path = Path("datasets/job_descriptions.csv")

# Check whether the file exists
if not file_path.exists():
    print("Dataset not found! Check your datasets folder.")
else:
    # Load the dataset
    df = pd.read_csv(file_path)

    print("DATASET LOADED SUCCESSFULLY!")

    # Display dataset information
    print("\nDataset shape:")
    print(df.shape)

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head().to_string())

    print("\nMissing values:")
    print(df.isnull().sum())
