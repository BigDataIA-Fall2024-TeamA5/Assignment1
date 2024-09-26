import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to connect to PostgreSQL and fetch the correct answer for the test case
def get_correct_answer_from_db(test_case):
    try:
        # Connect to PostgreSQL using environment variables
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        )
        cursor = conn.cursor()

        # Query to fetch the correct answer for the selected test case
        cursor.execute("SELECT CorrectAnswer FROM gaia_validation WHERE Question = %s", (test_case,))
        row = cursor.fetchone()

        # Close the connection
        cursor.close()
        conn.close()

        # Return the correct answer (if found)
        if row:
            return row[0]  # Return the correct answer from the first column
        else:
            return "No correct answer found for this test case."
    
    except Exception as e:
        st.error(f"Error fetching correct answer: {e}")
        return None

# Function for validation page
def validation_page():
    # Check if the required session state variables are available
    if 'selected_case' not in st.session_state or 'chatgpt_response' not in st.session_state:
        st.error("No test case or ChatGPT response available. Please go back and select a test case.")
        st.stop()

    # Retrieve the selected test case and ChatGPT response from session state
    selected_case = st.session_state['selected_case']
    chatgpt_response = st.session_state['chatgpt_response']

    # Display the selected test case
    st.subheader(f"Validating Test Case: {selected_case}")
    st.write(f"Selected Test Case: {selected_case}")

    # Display the ChatGPT response
    st.write(f"ChatGPT Response: {chatgpt_response}")

    # Fetch the correct answer from the GAIA dataset
    correct_answer = get_correct_answer_from_db(selected_case)
    st.write(f"Correct Answer from GAIA Dataset: {correct_answer}")

    # Correct/Incorrect buttons for validation
    st.write("Is the ChatGPT response correct?")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Correct"):
            st.write("Response marked as correct!")
            # Logic to store the result in the database as correct
            st.session_state['validation_result'] = "Correct"
            st.experimental_rerun()  # Optionally rerun if needed

    with col2:
        if st.button("Incorrect"):
            st.write("Response marked as incorrect!")
            # Logic to store the result in the database as incorrect
            st.session_state['validation_result'] = "Incorrect"
            st.experimental_rerun()  # Optionally rerun if needed

# Call the function to display the page content
validation_page()
