# RAG Model Evaluation Tool

This project is designed to build a tool for the evaluation of Retrieval-Augmented Generation (RAG) models using Streamlit and various cloud resources like AWS S3, PostgreSQL RDS, and OpenAI's GPT models.

## Codelabs Link:

[Codelabs Link](https://codelabs-preview.appspot.com/?file_id=1mjSKMWLaBjHpahLFToNlpkTMapciBedKwfLZGAjF07A#0)

## Link for Video Submission: 

[Video Submission](https://drive.google.com/file/d/19I_VNQc1OnEuPOMaJiJlypfMIwDwJnSX/view?usp=sharing)

## Link to Working Project:

[Deployment link](https://rag-model-eval.streamlit.app/)


## Github project link:

[Github Link](https://github.com/BigDataIA-Fall2024-TeamA5/Assignment1.git)

## Project Structure

This repository contains the following directories and files:

```bash
RAG_Model_Eval
├── .DS_Store
├── .env
├── Architecture
│   ├── Architecture_Diagram.ipynb
│   ├── Streamlit.png
│   ├── fall 24 bill.pdf
│   ├── hugging_face.avif
│   ├── openai.png
│   └── streamlit_workflow_architecture.png
├── AWS_S3
├── CreateTablesthruCSV.py
├── DownloadFromS3.py
├── FastAPI
│   └── pyproject.toml
├── LICENSE.md
├── LoadToDatabase.py
├── LoadToS3.py
├── RAG_Model_Eval.lock
├── README.md
├── Streamlit_app
│   ├── .DS_Store
│   ├── .env
│   ├── assignment_env
│   │   ├── Lib/site-packages
│   │   ├── Scripts
│   │   └── Views
│   │       ├── __pycache__
│   │       ├── About_page.py
│   │       ├── Application_page.py
│   │       ├── Info_page.py
│   │       ├── Main_page.py
│   │       └── Visualization.py
│   ├── app.py
│   ├── pyvenv.cfg
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── s3_connection_test.py
│   └── tree.txt
├── data.py
├── gaia_test_dataset.csv
├── gaia_validation_dataset.csv
├── insertDatatoRDS.py
├── poetry.lock
├── pyproject.toml
└── tree.txt
```

## Project Files Description

### Root Directory
- **`.env`**: Contains environment variables for AWS and database connections.
- **`CreateTablesthruCSV.py`**: Script to create PostgreSQL tables using CSV data.
- **`DownloadFromS3.py`**: Script to download files from AWS S3.
- **`LoadToDatabase.py`**: Script to load data into the database from CSV files.
- **`LoadToS3.py`**: Script to upload files to AWS S3.
- **`insertDatatoRDS.py`**: Script to insert data into AWS RDS.

### `Streamlit_app` Directory
This is the main directory for the Streamlit app and its components.

- **`assignment_env`**: Virtual environment setup for the app.
  - **`Lib/site-packages`**: Installed packages.
  - **`Scripts`**: Script files.
  - **`Views`**: Contains the different views/pages of the app.
    - **`About_page.py`**: About page script.
    - **`Application_page.py`**: Main application page for test case evaluation.
    - **`Info_page.py`**: Information page.
    - **`Main_page.py`**: Entry point for the app.
    - **`Visualization.py`**: Visualization page for dashboard display.
- **`app.py`**: Entry point for the Streamlit app.
- **`s3_connection_test.py`**: Script to test S3 connectivity.
- **`poetry.lock`**: Poetry dependency lock file.
- **`pyproject.toml`**: Poetry configuration file.
- **`tree.txt`**: Text file representation of the folder structure.

### `Architecture` Directory
Contains architecture-related files, including diagrams and images.
- **`Architecture_Diagram.ipynb`**: Jupyter notebook with architecture diagrams.
- **`Streamlit.png`**: Image file for Streamlit architecture.
- **`fall 24 bill.pdf`**: Miscellaneous PDF file.
- **`hugging_face.avif`**: Image related to the Hugging Face model.
- **`openai.png`**: OpenAI architecture image.
- **`streamlit_workflow_architecture.png`**: Streamlit workflow image.

### `FastAPI` Directory
Contains FastAPI configuration files.
- **`pyproject.toml`**: FastAPI project configuration.

### Data Files
- **`gaia_test_dataset.csv`**: GAIA test dataset CSV.
- **`gaia_validation_dataset.csv`**: GAIA validation dataset CSV.

## How to Run the Application

### Prerequisites
- Install [Poetry](https://python-poetry.org/) for dependency management.
- Ensure you have a `.env` file with the following environment variables:

  ```bash
  AWS_ACCESS_KEY_ID=<your-access-key-id>
  AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
  POSTGRES_HOST=<your-rds-host>
  POSTGRES_DB=<your-database>
  POSTGRES_USER=<your-username>
  POSTGRES_PASSWORD=<your-password>
  OPENAI_API_KEY=<your-openai-api-key>
  ```

### Setup and Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/RAG_Model_Eval.git
   cd RAG_Model_Eval
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```

3. **Run the Streamlit App:**
   ```bash
   streamlit run Streamlit_app/app.py
   ```



### Contribution
1. Saurabh Vyawahare - 40%
2. Aniket Patole - 40%
3. Shreya Bage - 20%

### Usage
1. Launch the app and log in using the required credentials.
2. Choose a test case from the dropdown menu.
3. If a file is associated with the test case, it will be fetched from S3 and processed.
4. Review the ChatGPT-generated response and validate the results.

## Contributing
1. Fork the project.
2. Create a feature branch.
3. Submit a pull request for review.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.
