import os
import json
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import datasets

_CITATION = """ """
_DESCRIPTION = """ """
_HOMEPAGE = ""
_LICENSE = ""

_NAMES = [
    "2023_all"
]

YEAR_TO_LEVELS = {"2023": [1, 2, 3]}
separator = "_"

# S3 Initialization
s3 = boto3.client('s3')

def upload_to_s3(local_file, bucket, s3_file):
    """Uploads a file to S3 bucket"""
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print(f"Upload Successful: {local_file} to s3://{bucket}/{s3_file}")
    except FileNotFoundError:
        print(f"The file {local_file} was not found")
    except NoCredentialsError:
        print("Credentials not available")
    except ClientError as e:
        print(f"Client error: {e}")

class GAIA_dataset(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("0.0.1")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name=name, version=version, description=name)
        for name, version in zip(_NAMES, [VERSION] * len(_NAMES))
    ]

    def _info(self):
        features = datasets.Features(
            {
                "task_id": datasets.Value("string"),
                "Question": datasets.Value("string"),
                "Level": datasets.Value("string"),
                "Final answer": datasets.Value("string"),  # ? for test values
                "file_name": datasets.Value("string"),
                "file_path": datasets.Value("string"),  # generated here
                "Annotator Metadata": {k: datasets.Value("string") for k in ["Steps", "Number of steps", "How long did this take?", "Tools", "Number of tools"]}
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        year, level_name = self.config.name.split(separator)
        if level_name == "all":
            levels = YEAR_TO_LEVELS[year]
        else:
            level_name = int(level_name.split("level")[1])
            levels = [level_name]
        print(year, level_name)

        output = []
        for split in ["test", "validation"]:
            # Download the main metadata file
            root_file = dl_manager.download(os.path.join(year, split, "metadata.jsonl"))
            
            # Dictionary to store attached file references
            test_attached_files = {"": ""}
            
            # Load metadata and download associated files
            with open(root_file, "r", encoding="utf-8") as f:
                for line in f:
                    cur_line = json.loads(line)
                    if cur_line["Level"] in levels and cur_line["file_name"] != "":
                        attached_file_name = cur_line["file_name"]
                        attached_file = dl_manager.download(os.path.join(year, split, attached_file_name))
                        test_attached_files[attached_file_name] = attached_file

                        # Upload each attached file to S3 under a folder
                        upload_to_s3(attached_file, "ragmodelbucket-fall2024-group5", f"GAIA_2023/{split}/{attached_file_name}")

            # Upload metadata JSONL file to S3
            upload_to_s3(root_file, "ragmodelbucket-fall2024-group5", f"GAIA_2023/{split}/metadata.jsonl")
            
            output.append(
                datasets.SplitGenerator(
                    name=getattr(datasets.Split, split.upper()),
                    gen_kwargs={"root_file": root_file, "attached_files": test_attached_files, "levels": levels},
                )
            )
        return output

    def _generate_examples(self, root_file: str, attached_files: dict, levels: list[int]):
        # Generate examples by yielding the data rows
        with open(root_file, "r", encoding="utf-8") as f:
            for key, line in enumerate(f):
                cur_line = json.loads(line)
                if cur_line["Level"] in levels:
                    # Link file paths and upload to S3 if needed
                    cur_line["file_path"] = attached_files[cur_line["file_name"]]
                    yield key, cur_line


if __name__ == "__main__":
    # Example: Load the '2023_all' configuration of the dataset
    config_name = '2023_all'  # Choose from '2023_all', '2023_level1', '2023_level2', '2023_level3'

    # Create the dataset builder for the chosen configuration
    builder = GAIA_dataset(config_name=config_name)

    # Download and prepare the dataset (this will download the data and prepare it for usage)
    print("Downloading and preparing the dataset...")
    builder.download_and_prepare()

    # Generate and process the dataset
    dataset = builder.as_dataset(split="test")

    print(f"Dataset with config {config_name} loaded successfully.")