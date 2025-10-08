import streamlit as st
from streamlit_javascript import st_javascript

if "page" not in st.session_state:
    st.session_state.page = 1

def login_page(): 
    with st.form("my_form"):
        tab1, tab2 = st.tabs(["Login", "Signup"])
        with tab1:
            login_username = ""
            st.header("Login")
            login_username = st.text_input(key="lu", label="Username")
            st.text_input(key="lp", label="Password")
        with tab2:
            signup_username = ""
            st.header("Signup")
            signup_username = st.text_input(key="su", label="Username")
            st.text_input(key="sp", label="Password")
        if signup_username:
            string = signup
        else if login_username:
            string = login
        else:
            string = "Submit"
        submitted = st.form_submit_button(string)
    if submitted:
        st.session_state.page = 0
        st.rerun()
