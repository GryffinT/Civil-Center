import streamlit as st
from supabase import create_client, Client
import bcrypt

if "page" not in st.session_state:
    st.session_state.page = 1

def login_page(): 
    # === Styles ===
    st.markdown("""
    <style>
    .css-18e3th9 {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    body {
        margin: 0;
    }
    
    /* Full-width frosted top bar */
    .top-bar {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 150px;
        display: flex;
        align-items: center;
        padding-left: 30px;
        z-index: 9999;
    
        background: rgba(220, 219, 218, 0.5);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Text inside the bar */
    .top-bar span {
        font-size: 50px;
        font-weight: bold;
        color: black;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        background: transparent !important;
    }
    
    /* Buttons */
    .top-bar button {
        margin-top: 60px;
        margin-right: 30px;
        padding: 10px 20px;
        font-size: 20px;
        background-color: #000;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: 0.2s;
    }
    
    .top-bar button:hover {
        background-color: #333;
    }
    
    /* Transparent Streamlit boxes */
    [data-testid="stTextInput"] > div:first-child, 
    [data-testid="stTextArea"] > div:first-child,
    .css-1adrfps {
        background-color: transparent !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # === HTML Layout ===
    st.markdown("""
    <div class="top-bar">
        <span style="padding-top: 60px;">Civil<sub>Center</sub></span>
    </div>
    <div style="height: 150px;"></div>
    """, unsafe_allow_html=True)
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase: Client = create_client(url, key)
    col1, col2, col3 = st.columns([2,5,2])
    
    with col1:
        pass
    with col2:
        with st.form("my_form"):
            st.markdown("<h1>Civil<sub>Center</sub></h1> ", unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["Login", "Register"])
            with tab1:
                signup_password = ""
                signup_username = ""
                st.header("Login")
                st.write("")
                login_username = st.text_input(key="lu", label="Username")
                st.write("")
                login_password = st.text_input(key="lp", label="Password", type="password")
                st.write("")
                submitted = st.form_submit_button(key="login", label="Login")
                if submitted:
                    if not (login_password and login_username):
                        st.error("Please fill in all fields.")
                    elif login_password and login_username:
                        response = supabase.table("users").select("*").eq("username", login_username).execute()
                        if response.data:
                            hashed_password = response.data[0]['password']
                            if bcrypt.checkpw(login_password.encode('utf-8'), hashed_password.encode('utf-8')):
                                st.success("Login successful!")
                                st.session_state.username = login_username
                                st.session_state.password = login_password
                                st.session_state.page = 2
                                st.rerun()
                            else:
                                st.error("Incorrect password.")
                        else:
                            st.error("Username not found.")
            with tab2:
                login_password = ""
                login_username = ""
                st.header("Register")
                st.write("")
                signup_username = st.text_input(key="su", label="Username")
                st.write("")
                signup_password = st.text_input(key="sp", label="Password", type="password")
                st.write("")
                submitted = st.form_submit_button(key="register", label="Register")
                if submitted:
                    if signup_password and signup_username:
                        response = supabase.table("users").select("*").eq("username", signup_username).execute()
                        if response.data:
                            st.error("Username already exists.")
                        else:
                            hashed_password = bcrypt.hashpw(signup_password.encode('utf-8'), bcrypt.gensalt())
                            supabase.table("users").insert({"username": signup_username, "password": hashed_password.decode('utf-8')}).execute()
                            st.success("Signup successful! Please log in.")
                            st.session_state.page = 0
                            st.rerun()
                    elif not (signup_password and signup_username):
                        st.error("Please fill in all fields.")

    with col3:
        pass
