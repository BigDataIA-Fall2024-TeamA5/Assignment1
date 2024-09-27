import streamlit as st

# Define your pages as before
main_page = st.Page(
    page="Views/Main_page.py",
    title="RAG Model Dashboard",
    icon=":material/dashboard:",
    default=True,
)

Project_side_page_1 = st.Page(
    page="Views/Info_page.py",
    title="Info",
    icon=":material/info:",
)

Project_side_page_2 = st.Page(
    page="Views/About_page.py",
    title="About us",
    icon=":material/group:",
)

visualization_for_data = st.Page(
    page="Views/Visualization.py",
    title="Visualization",
    icon=":material/insights:",
)

# Navigation setup
pg = st.navigation(pages=[main_page, Project_side_page_1, Project_side_page_2, visualization_for_data])

# Handle page navigation using session state
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Views/Main_page.py'  # Set default page

# Set the page based on session state
pg.run()
