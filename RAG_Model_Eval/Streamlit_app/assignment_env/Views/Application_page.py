"""import streamlit as st

# Function for application page
def application_page():
    # Add logout button in the sidebar
    with st.sidebar:
        if st.button("Logout"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()  # Use st.rerun instead of experimental_rerun for logout.

    st.subheader(f"Welcome, {st.session_state['user']}!")

    # Dropdown to select a test case from GAIA dataset
    test_cases = ["Test Case 1", "Test Case 2", "Test Case 3"]  # Replace with real test cases
    selected_case = st.selectbox("Select a test case", test_cases)

    # Create two columns for the buttons
    col1, col2 = st.columns([2, 10])

    # Button to validate the selected test case in the first column
    with col1:
        if st.button("Validate"):
            st.write(f"Validating: {selected_case}")
            # Logic for validating the selected test case

    # Visualization button placed slightly lower and in the second column
    with col2:
        if st.button("Visualization"):
            st.write("Visualization functionality will be added here.")
            # Logic for visualization

    # Placeholder for future navigation (additional pages)
    if st.button("Go to Other Page"):
        st.write("This button will navigate to a new page in the future.")


import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to connect to PostgreSQL and fetch test cases
def get_test_cases_from_db():
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

        # Execute the query to fetch the 'Question' column from 'gaia_validation' table
        cursor.execute("SELECT Question FROM gaia_validation")
        rows = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()

        # Return a list of questions (test cases)
        return [row[0] for row in rows]  # Extract the first column (Question)
    
    except Exception as e:
        st.error(f"Error fetching test cases: {e}")
        return []

# Function for the application page
def application_page():
    # Add logout button in the sidebar
    with st.sidebar:
        if st.button("Logout"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()  # Use st.rerun instead of experimental_rerun for logout.

    st.subheader(f"Welcome, {st.session_state['user']}!")

    # Fetch test cases from PostgreSQL
    test_cases = get_test_cases_from_db()
    
    if test_cases:
        # Dropdown to select a test case from the fetched data
        selected_case = st.selectbox("Select a test case", test_cases)

        # Create two columns for the buttons
        col1, col2 = st.columns([2, 10])

        # Button to validate the selected test case in the first column
        with col1:
            if st.button("Validate"):
                st.write(f"Validating: {selected_case}")
                # Logic for validating the selected test case

        # Visualization button placed slightly lower and in the second column
        with col2:
            if st.button("Visualization"):
                st.write("Visualization functionality will be added here.")
                # Logic for visualization

        # Placeholder for future navigation (additional pages)
        if st.button("Go to Other Page"):
            st.write("This button will navigate to a new page in the future.")
    else:
        st.warning("No test cases available.")

if __name__ == "__main__":
    application_page()
    """
 # -- working application page -- #
"""import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to connect to PostgreSQL and fetch test cases
def get_test_cases_from_db():
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

        # Execute the query to fetch the 'Question' column from 'gaia_validation' table
        cursor.execute("SELECT Question FROM gaia_validation")
        rows = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()

        # Return a list of questions (test cases)
        return [row[0] for row in rows]  # Extract the first column (Question)
    
    except Exception as e:
        st.error(f"Error fetching test cases: {e}")
        return []

# Function for the application page
def application_page():
    # Add logout button in the sidebar
    with st.sidebar:
        if st.button("Logout"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()  # Use st.rerun instead of experimental_rerun for logout.

    # Display welcome message
    st.subheader(f"Welcome, {st.session_state.get('user', 'User')}!")  # Using .get() for fallback

    # Fetch test cases from PostgreSQL
    test_cases = get_test_cases_from_db()
    
    if test_cases:
        # Dropdown to select a test case from the fetched data
        selected_case = st.selectbox("Select a test case", test_cases)

        # Create two columns for the buttons
        col1, col2 = st.columns([2, 10])

        # Button to validate the selected test case in the first column
        with col1:
            if st.button("Validate"):
                st.write(f"Validating: {selected_case}")
                # Logic for validating the selected test case (future implementation)

        # Visualization button placed slightly lower and in the second column
        with col2:
            if st.button("Visualization"):
                st.write("Visualization functionality will be added here.")
                # Logic for visualization (future implementation)

        # Placeholder for future navigation (additional pages)
        if st.button("Go to Other Page"):
            st.write("This button will navigate to a new page in the future.")
    else:
        st.warning("No test cases available.")

# Main execution of the Streamlit app
if __name__ == "__main__":
    # Check if user is logged in before showing the application page
    if 'user' in st.session_state:
        application_page()
    else:
        st.error("You need to be logged in to view this page.")"""

# -- with OPenai api code -- #

import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Function to connect to PostgreSQL and fetch test cases
def get_test_cases_from_db():
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT Question FROM gaia_validation")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [row[0] for row in rows]  # Return list of questions
    except Exception as e:
        st.error(f"Error fetching test cases: {e}")
        return []

# Function to fetch the correct answer from the database
def get_correct_answer_from_db(test_case):
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        )
        cursor = conn.cursor()
        cursor.execute('SELECT Final answer FROM gaia_validation WHERE Question = %s', (test_case,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row[0] if row else "No correct answer found."
    except Exception as e:
        st.error(f"Error fetching correct answer: {e}")
        return None

# Main function for the application page
def application_page():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Fetch test cases
    test_cases = get_test_cases_from_db()

    if test_cases:
        # Step 1: Test Case Selection
        selected_case = st.selectbox("Select a test case", test_cases, key="test_case_select")

        # Step 2: Fetch ChatGPT response
        if st.button("Validate") or ('chatgpt_response' in st.session_state and st.session_state.get('selected_case') == selected_case):
            st.session_state['selected_case'] = selected_case
            
            if 'chatgpt_response' not in st.session_state or st.session_state['selected_case'] != selected_case:
                st.write(f"Validating: {selected_case}")
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are an AI that helps answer test cases."},
                            {"role": "user", "content": f"Answer the following test case: {selected_case}"}
                        ]
                    )
                    st.session_state['chatgpt_response'] = response.choices[0].message.content.strip()
                except Exception as e:
                    st.error(f"Error calling OpenAI API: {e}")
                    return

            # Step 3: Display Test Case and Responses
            st.subheader(f"Test Case: {selected_case}")
            st.write(f"ChatGPT Response: {st.session_state['chatgpt_response']}")

            # Fetch the correct answer from the database if not already in session state
            if 'correct_answer' not in st.session_state or st.session_state['selected_case'] != selected_case:
                st.session_state['correct_answer'] = get_correct_answer_from_db(selected_case)

            # Display non-editable text area for the correct answer
            st.subheader("Correct Answer (GAIA dataset)")
            st.text_area("", value=st.session_state['correct_answer'], height=150, disabled=True)

            # Step 4: Validation Buttons
            st.write("Is the ChatGPT response correct?")
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Correct"):
                    st.success("You marked the response as Correct.")

            with col2:
                if st.button("Incorrect"):
                    st.error("You marked the response as Incorrect.")

    else:
        st.warning("No test cases available.")

# Main execution
if 'user' in st.session_state:
    application_page()
else:
    st.error("You need to be logged in to view this page.")










