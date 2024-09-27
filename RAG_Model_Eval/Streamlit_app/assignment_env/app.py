import streamlit as st


# -- PAGE SETUP -- #

main_page = st.Page(
    page = "Views/Main_page.py",
    title = "RAG Model Dashboard",
    icon = ":material/dashboard:",  # Changed to 'dashboard' icon
    default = True,
)

Project_side_page_1 = st.Page(
    page = "Views/Info_page.py",
    title = "Info",
    icon = ":material/info:",  # Changed to 'info' icon
)

Project_side_page_2 = st.Page(
    page = "Views/About_page.py",
    title = "About us",
    icon = ":material/group:",  # Changed to 'group' icon
)

visualization_for_data = st.Page(
    page = "Views/Visualization.py",
    title = "Visualization",
    icon = ":material/insights:",  # Changed to 'insights' icon
)

# -- Navigation section -- #

pg = st.navigation( pages= [main_page, Project_side_page_1, Project_side_page_2, visualization_for_data])

pg.run()