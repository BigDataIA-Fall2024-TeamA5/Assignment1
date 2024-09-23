import streamlit as st

# Title of the page
st.title("Assignment 1 - RAG Model Evaluation Analysis Tool")

# Authors section
st.markdown("""
### Authors:
- **Aniket Patole**
- **Saurabh Vyawahare**
- **Shreya Bage**
""")

# Introduction
st.header("Introduction")
st.write("""
This project involves building a model evaluation tool using Streamlit to assess the performance of OpenAI's language models against test cases from the GAIA dataset. 
Users can interactively select test cases, compare model responses, and provide feedback to improve model accuracy.
""")

# Technologies Used
st.subheader("Technologies Used and Their Roles:")
st.markdown("""
- **Hugging Face**: Provides access to the GAIA dataset for test case selection and model evaluation.
- **PostgreSQL**: Manages structured data, including user inputs, model responses, and feedback for persistent storage.
- **Amazon S3**: Stores unstructured data such as larger datasets, logs, and temporary files.
- **OpenAI API**: Generates model responses based on the selected test cases from the GAIA dataset.
- **Streamlit**: Serves as the frontend interface where users interact with the system, choose test cases, and view results.
- **PowerBI**: Generates analytical reports and visualizations based on the evaluation results and feedback provided by users.
""")

# Goal of the Project
st.header("Goal of the Project")
st.write("""
The goal is to create a streamlined tool for evaluating and comparing model responses, enabling users to provide feedback and improve model accuracy.
The tool will support data-driven insights and real-time analytics, facilitating more informed decision-making.
""")

# Problem Statement
st.header("Problem Statement")
st.write("""
The challenge addressed by this project is the need for an efficient and interactive tool to evaluate the performance of OpenAI's language models against specific test cases from the GAIA dataset. 
Currently, the process of manually comparing model responses with test case data and iterating through feedback is time-consuming and lacks automation. Additionally, there is no straightforward system for users to provide feedback on incorrect responses and re-evaluate the model based on this feedback.

The desired outcome is to create an automated evaluation tool that allows users to select test cases, compare OpenAI model outputs with expected results, and provide feedback when discrepancies are identified. 
This feedback loop will improve the model's performance by allowing re-evaluation with modified annotations and steps. 
The system should also generate insightful reports and visualizations to track model accuracy and feedback over time.
""")

# Proof of Concept
st.header("Proof of Concept")
st.write("""
The solution to this problem relies on the integration of several technologies that work together to automate and streamline the model evaluation process. 
The primary technologies involved include Streamlit for the frontend interface, Hugging Face for accessing the GAIA dataset, OpenAI API for generating model responses, PostgreSQL for structured data management, Amazon S3 for unstructured data storage, and PowerBI for reporting and analytics.
""")

st.markdown("""
- **Streamlit** is chosen for its ease of use in building interactive web applications with Python, providing an intuitive interface for users to select test cases, submit them to the OpenAI model, and view results.
- **Hugging Face's GAIA dataset** is selected as the source of test cases, as it provides robust and diverse datasets for model evaluation.
- **PostgreSQL and Amazon S3** are essential for data management; PostgreSQL handles structured data such as user inputs and model responses, while Amazon S3 is used to store unstructured data, such as larger datasets and logs.
- **OpenAI API** is used for generating model outputs, with its strong language processing capabilities making it ideal for responding to user-selected test cases.
- **PowerBI** is utilized for visualizing feedback and results, enabling users to derive insights from the model evaluations and feedback loops.
""")

st.write("""
Challenges anticipated include handling large datasets from Hugging Face and ensuring seamless, real-time interaction with the OpenAI API without latency issues. These will be addressed by implementing efficient data retrieval methods and utilizing caching where necessary.
Another challenge is ensuring non-technical users can easily navigate the interface, which will be handled through user-centric design in the Streamlit app, ensuring a smooth experience.
""")

# Architecture Diagram
st.header("Architecture Diagram")
st.write("""
Provide a high-level visual representation of the entire system architecture. This diagram helps readers understand how the components interact and what role each one plays.

What to include:
- A labeled diagram showing all the major components (Frontend, Backend, Pipeline, Database, AI, etc.)
- Description of each component and its role in the system
- Data flow and interactions between the components
""")

# Walkthrough of the Application
st.header("Walkthrough of the Application (with snapshots and explanation)")
st.write("""
In this section, guide the reader through the function of the application step-by-step. Include snapshots of user interfaces to clarify each step.

What to include:
- Step-by-step instructions to implement the project
- Screenshots of the application in action (e.g., UI snapshots, command line outputs)
""")

# Application Workflow
st.header("Application Workflow (Data Engineering Work + Code Explanation)")
st.write("""
This section explains the backend processes and the overall workflow of the application, particularly the data engineering tasks. Focus on how data flows through the system and the backend processing that takes place.

What to include:
- Explanation of the full data flow, from frontend input to backend processing and final output
- Details about pipeline orchestration (Airflow DAGs, task scheduling)
- Backend architecture and API layer (FastAPI setup, database interactions)
- Code snippets for key tasks such as data processing, storage, and retrieval
- Challenges faced during implementation and how they were solved
""")

# References
st.header("References")
st.write("""
Provide a list of references for any tools, documentation, or external resources used during the project.

What to include:
- Links to official documentation for the technologies used
- Tutorials, blog posts, or articles that were useful during development
- Any additional resources or reading material relevant to the project
""")
