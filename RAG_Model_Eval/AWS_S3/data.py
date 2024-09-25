from datasets import load_dataset

# Load the dataset
ds = load_dataset("gaia-benchmark/GAIA", "2023_all")

# Specify the save path for each split
csv_path_test = "/Users/aniketpatole/Documents/GitHub/New/Projects/BigData/Assignment1/RAG_Model_Eval/AWS_S3/gaia_test_dataset.csv"
csv_path_validation = "/Users/aniketpatole/Documents/GitHub/New/Projects/BigData/Assignment1/RAG_Model_Eval/AWS_S3/gaia_validation_dataset.csv"

# Save the 'test' split as a CSV file
ds['test'].to_csv(csv_path_test)

# Save the 'validation' split as a CSV file
ds['validation'].to_csv(csv_path_validation)

print(f"Test dataset saved to {csv_path_test}")
print(f"Validation dataset saved to {csv_path_validation}")