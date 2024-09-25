import streamlit as st

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
