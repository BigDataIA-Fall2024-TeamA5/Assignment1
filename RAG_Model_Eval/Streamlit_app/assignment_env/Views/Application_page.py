import streamlit as st

# Function for application page
def application_page():
    st.subheader(f"Welcome, {st.session_state['user']}!")

    # Dropdown to select a test case from GAIA dataset
    test_cases = ["Test Case 1", "Test Case 2", "Test Case 3"]  # Replace with real test cases
    selected_case = st.selectbox("Select a test case", test_cases)

    # Button to validate the selected test case
    if st.button("Validate"):
        st.write(f"Validating: {selected_case}")
        # Logic for validating the selected test case

    # Placeholder for future navigation (additional pages)
    if st.button("Go to Other Page"):
        st.write("This button will navigate to a new page in the future.")
