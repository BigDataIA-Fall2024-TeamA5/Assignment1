import streamlit as st
import psycopg2
import bcrypt
from Views.Application_page import application_page

# Function to connect to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        host="damg7245-bigdata-team5-assignment1.cpiiiaekyr9u.us-east-1.rds.amazonaws.com",
        database="damg7245_assignment1_database",
        user="postgres",
        password="Tiger441saurabh",
        port="5432"
    )
    return conn

# -- For Signup User -- #
def signup(username, full_name, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        st.error("Username already exists. Please choose a different one.")
    else:
        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert the new user into the database
        cursor.execute("""
            INSERT INTO users (username, name, hashed_password) 
            VALUES (%s, %s, %s)
        """, (username, full_name, hashed_password.decode('utf-8')))
        
        conn.commit()  # Save the changes to the database
        st.success(f"Account created for {full_name}!")
        st.write("You can now log in with your credentials.")

    cursor.close()
    conn.close()

# -- For Login User -- #
def login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the hashed password and full name for the given username
    cursor.execute("SELECT name, hashed_password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user:
        full_name, stored_hashed_password = user
        # Verify the password
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            st.success(f"Welcome back, {full_name}!")
            st.session_state['logged_in'] = True
            st.session_state['user'] = full_name
            st.session_state['page'] = 'application'  # Set to application page
        else:
            st.error("Incorrect password. Please try again.")
    else:
        st.error("Username not found. Please try again.")

    cursor.close()
    conn.close()

# -- Application Page -- #
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'page' not in st.session_state:
    st.session_state['page'] = 'login'  # Default to login page

# Page Navigation based on session state
if st.session_state['logged_in']:
    application_page()  # Call the function from application_page.py
else:
    option = st.selectbox("Select Login or Signup", ("Login", "Signup"))

    if option == "Login":
        st.subheader("Login")
        username = st.text_input("Email ID / Username")
        password = st.text_input("Password", type="password")  # Hide the password input
        
        if st.button("Login"):
            login(username, password)  # Call the login function

    elif option == "Signup":
        st.subheader("Signup")
        username = st.text_input("Email ID / Username")
        full_name = st.text_input("Full Name")
        password = st.text_input("Password", type="password")  # Hide the password input
        
        if st.button("Signup"):
            signup(username, full_name, password)