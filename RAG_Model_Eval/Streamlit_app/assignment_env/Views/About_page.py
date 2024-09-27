import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="About Us",
    page_icon=":group:",  # Use a group icon
    layout="centered",
)

# Page Title
st.title("About Us")

# Project Overview
st.markdown("""
### Project Title: RAG Model Evaluation Analysis Tool
This project is a part of the Fall 2024 Data Engineering course at Northeastern University.
It aims to build a model evaluation tool to assess the performance of OpenAI's language models against test cases from the GAIA dataset.
Users can select test cases, compare model responses, and provide feedback to improve model accuracy.
""")

# Purpose and Goals
st.subheader("Purpose and Goals")
st.markdown("""
The tool serves as an interactive platform to streamline the process of model evaluation by providing:
- Real-time comparisons of OpenAI responses against test cases.
- An intuitive interface to submit feedback and suggestions.
- Enhanced data-driven insights through visualizations and analytical reports.
""")

# Technologies Used
st.subheader("Technologies Used")
st.markdown("""
- **Hugging Face**: Provides access to the GAIA dataset for test case selection.
- **PostgreSQL**: Manages structured data, including user inputs, model responses, and feedback.
- **Amazon S3**: Stores unstructured data such as larger datasets, logs, and temporary files.
- **OpenAI API**: Generates model responses based on the selected test cases.
- **Streamlit**: Serves as the frontend interface for interaction and visualization.
- **PowerBI**: Generates analytical reports and visualizations based on evaluation results.
""")

# Team Members
st.subheader("Team Members")
st.markdown("""
- **Aniket Patole**: Backend & API Integration
- **Saurabh Vyawahare**: Data Management, User Interface & Project Coordination
- **Shreya Bage**: Documentation & Visualization
""")

# Footer
st.markdown("""
---  
© 2024 RAG Model Evaluation Analysis Tool. All rights reserved.
""")
