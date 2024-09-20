import streamlit as st

# Simulating a user database with a dictionary
user_database = {}

def login(username, password):
    if username in user_database and user_database[username]["password"] == password:
        st.success(f"Welcome back, {user_database[username]['name']}!")
        st.write("You are successfully logged in.")
    else:
        st.error("Incorrect username or password. Please try again.")

def signup(username, full_name, password):
    if username in user_database:
        st.error("Username already exists. Please choose a different one.")
    else:
        user_database[username] = {"name": full_name, "password": password}
        st.success(f"Account created for {full_name}!")
        st.write("You can now log in with your credentials.")

# Creating Login/Signup interface
st.title("Login / Signup Page")

option = st.selectbox("Select Login or Signup", ("Login", "Signup"))

if option == "Login":
    st.subheader("Login")
    username = st.text_input("Email ID / Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        login(username, password)

elif option == "Signup":
    st.subheader("Signup")
    username = st.text_input("Email ID / Username")
    full_name = st.text_input("Full Name")
    password = st.text_input("Password", type="password")
    
    if st.button("Signup"):
        signup(username, full_name, password)