import streamlit as st

# -- PAGE SETUP -- #

main_page = st.Page(
    page = "Views/Main_page.py",
    title = "RAG Model Dashboard",
    icon = ":material/account_circle:",
    default = True,
)

Project_side_page_1 = st.Page(
    page = "Views/Info_page.py",
    title = "Info",
    icon = ":material/bar_chart:",
)

Project_side_page_2 = st.Page(
    page = "Views/About_page.py",
    title = "About us",
    icon = ":material/smart_toy:",
)

# -- Navigation section -- #

pg = st.navigation( pages= [main_page, Project_side_page_1, Project_side_page_2])

pg.run()