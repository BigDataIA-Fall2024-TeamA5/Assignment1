import streamlit as st
import psycopg2
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Function to log out by clearing the session state
def logout():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

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
        cursor.execute("SELECT task_id, question FROM gaia_validation")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows  # Return list of task_id and questions
    except Exception as e:
        st.error(f"Error fetching test cases: {e}")
        return []

# Function to fetch the correct answer and annotator metadata from the database
def get_correct_answer_and_metadata_from_db(test_case):
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        )
        cursor = conn.cursor()
        cursor.execute('SELECT final_answer, annotator_metadata FROM gaia_validation WHERE question = %s', (test_case,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row if row else ("No correct answer found.", None)
    except Exception as e:
        st.error(f"Error fetching correct answer: {e}")
        return None, None

# Function to store the validation result in the gaia_validation_dashboard
def store_validation_result(task_id, validated=False, validated_with_help=False, not_validated=False):
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        )
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO gaia_validation_dashboard (task_id, validated, validated_with_help, not_validated)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (task_id) 
            DO UPDATE SET validated = EXCLUDED.validated, validated_with_help = EXCLUDED.validated_with_help, not_validated = EXCLUDED.not_validated
        """, (task_id, validated, validated_with_help, not_validated))

        conn.commit()
        cursor.close()
        conn.close()
        st.success(f"Validation result stored for task ID: {task_id}")
    except Exception as e:
        st.error(f"Error storing validation result: {e}")

# Main function for the application page
def application_page():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Add a sidebar with a logout button
    with st.sidebar:
        if st.button("Logout"):
            logout()

    # Fetch test cases
    test_cases = get_test_cases_from_db()

    if test_cases:
        # Create a dictionary of test cases for easy lookup
        test_case_dict = {row[1]: row[0] for row in test_cases}

        # Step 1: Test Case Selection
        selected_case = st.selectbox("Select a test case", list(test_case_dict.keys()), key="test_case_select")

        # Clear session states when a new test case is selected
        if 'selected_case' not in st.session_state or st.session_state['selected_case'] != selected_case:
            st.session_state['selected_case'] = selected_case
            st.session_state['show_hint'] = False  # Reset this flag for a new test case
            st.session_state['hide_chatgpt_response'] = False  # Ensure we are not hiding initially
            st.session_state['hide_validation_buttons'] = False  # Ensure the buttons are visible initially
            st.session_state['hide_validate_button'] = False  # Ensure the validate button is visible initially
            st.session_state['second_validate'] = False  # Reset second validation state
            if 'chatgpt_response' in st.session_state:
                del st.session_state['chatgpt_response']
            if 'correct_answer' in st.session_state:
                del st.session_state['correct_answer']
            if 'annotator_metadata' in st.session_state:
                del st.session_state['annotator_metadata']

        # Step 2: Fetch ChatGPT response
        if not st.session_state.get('hide_validate_button') and (st.button("Validate") or ('chatgpt_response' in st.session_state and st.session_state.get('selected_case') == selected_case)):
            if 'chatgpt_response' not in st.session_state:
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "system", "content": "You are an AI that helps answer test cases."},
                                  {"role": "user", "content": f"Answer the following test case: {selected_case}"}]
                    )
                    st.session_state['chatgpt_response'] = response.choices[0].message.content.strip()
                except Exception as e:
                    st.error(f"Error calling OpenAI API: {e}")
                    return

            # Step 3: Display ChatGPT Response if "Incorrect" button hasn't been pressed
            if not st.session_state.get('hide_chatgpt_response'):
                st.markdown("<h3 style='color: white;'>ChatGPT Response:</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:22px; color: white;'>{st.session_state['chatgpt_response']}</div>", unsafe_allow_html=True)

            # Fetch the correct answer and annotator metadata from the database
            correct_answer, annotator_metadata = get_correct_answer_and_metadata_from_db(selected_case)
            st.session_state['correct_answer'] = correct_answer
            st.session_state['annotator_metadata'] = annotator_metadata

            # Always display non-editable text area for the correct answer with a unique key
            st.subheader("Correct Answer (GAIA dataset)")
            st.text_area("Correct Answer", value=correct_answer, height=150, disabled=True, key="unique_correct_answer")

            # Step 4: Validation Buttons
            if not st.session_state.get('hide_validation_buttons'):
                st.write("Is the ChatGPT response correct?")
                col1, col2 = st.columns(2)

                task_id = test_case_dict[selected_case]  # Get the task_id for the selected case

                with col1:
                    if st.button("Correct"):
                        store_validation_result(task_id, validated=True)
                        st.success("You marked the response as Correct.")

                with col2:
                    if st.button("Incorrect"):
                        # Hide ChatGPT response and validation buttons, but keep the correct answer visible
                        st.session_state['show_hint'] = True
                        st.session_state['hide_chatgpt_response'] = True
                        st.session_state['hide_validation_buttons'] = True
                        st.session_state['hide_validate_button'] = True

        # Display the hint text area when "Incorrect" is pressed
        if st.session_state.get('show_hint'):
            st.subheader("Annotator Metadata (Editable)")
            new_metadata = st.text_area("Editable Metadata", value=st.session_state['annotator_metadata'], key="editable_metadata_unique")

            if st.button("Validate with Edited Metadata"):
                try:
                    response_with_hint = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "system", "content": "You are an AI that helps answer test cases."},
                                {"role": "user", "content": f"Test case: {selected_case}. Hint: {new_metadata}"}]
                    )
                    st.session_state['chatgpt_response_with_hint'] = response_with_hint.choices[0].message.content.strip()
                    st.session_state['second_validate'] = True  # Mark that second validation is complete
                except Exception as e:
                    st.error(f"Error calling OpenAI API with hint: {e}")

            # Display ChatGPT Response after hint
            if st.session_state.get('second_validate'):
                st.markdown("<h3 style='color: white;'>ChatGPT Response (with hint):</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:22px; color: white;'>{st.session_state['chatgpt_response_with_hint']}</div>", unsafe_allow_html=True)

                # Correct Answer is still visible after hint is used
                st.subheader("Correct Answer (GAIA dataset)")
                st.text_area("Correct Answer", value=st.session_state['correct_answer'], height=150, disabled=True, key="second_unique_correct_answer")

                # Step 5: Additional Validation Buttons after hint
                st.write("Is the ChatGPT response correct now?")
                col3, col4 = st.columns(2)

                with col3:
                    if st.button("Validated with Help"):
                        task_id = test_case_dict[selected_case]
                        store_validation_result(task_id, validated_with_help=True)
                        st.success("You marked the response as Correct with help.")

                with col4:
                    if st.button("Incorrect Again"):
                        task_id = test_case_dict[selected_case]
                        store_validation_result(task_id, not_validated=True)
                        st.error("You marked the response as Incorrect again.")

    else:
        st.warning("No test cases available.")

# Main execution
if 'user' in st.session_state:
    application_page()
else:
    st.error("You need to be logged in to view this page.")
