import streamlit as st
from supabase import create_client, Client
import bcrypt

if "page" not in st.session_state:
    st.session_state.page = 1

def login_page(): 
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase: Client = create_client(url, key)
    col1, col2, col3 = st.columns([2,5,2])
    
    with col1:
        pass
    with col2:
        with st.form("my_form"):
            tab1, tab2 = st.tabs(["Login", "Signup"])
            with tab1:
                signup_password = ""
                signup_username = ""
                st.header("Login")
                st.write("")
                login_username = st.text_input(key="lu", label="Username")
                st.write("")
                login_password = st.text_input(key="lp", label="Password")
                st.write("")
                submitted = st.form_submit_button(key="login", label="Submit")
            with tab2:
                login_password = ""
                login_username = ""
                st.header("Signup")
                st.write("")
                signup_username = st.text_input(key="su", label="Username")
                st.write("")
                signup_password = st.text_input(key="sp", label="Password")
                st.write("")
                submitted = st.form_submit_button(key="register", label="Submit")
        if submitted:
            if login_password and login_username:
                response = supabase.table("users").select("*").eq("username", login_username).execute()
                if response.data:
                    hashed_password = response.data[0]['password']
                    if bcrypt.checkpw(login_password.encode('utf-8'), hashed_password.encode('utf-8')):
                        st.success("Login successful!")
                        st.session_state.username = login_username
                        st.session_state.page = 2
                        st.rerun()
                    else:
                        st.error("Incorrect password.")
                else:
                    st.error("Username not found.")
            elif signup_password or signup_username:
                response = supabase.table("users").select("*").eq("username", signup_username).execute()
                if response.data:
                    st.error("Username already exists.")
                else:
                    hashed_password = bcrypt.hashpw(signup_password.encode('utf-8'), bcrypt.gensalt())
                    supabase.table("users").insert({"username": signup_username, "password": hashed_password.decode('utf-8')}).execute()
                    st.success("Signup successful! Please log in.")
                    st.session_state.page = 0
                    st.rerun()
            elif not (login_password or login_username or signup_password or signup_username):
                st.error("Please fill in all fields.")
            else:
                st.error("ERROR")

    with col3:
        pass
