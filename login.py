import streamlit as st
from streamlit_javascript import st_javascript

if "page" not in st.session_state:
    st.session_state.page = 1

def login_page(): 
    col1, col2, col3 = st.columns([2,5,2])
    
    with col1:
        pass
    with col2:
        with st.form("my_form"):
            tab1, tab2 = st.tabs(["Login", "Signup"])
            with tab1:
                login_username = ""
                st.header("Login")
                st.write("")
                login_username = st.text_input(key="lu", label="Username")
                st.write("")
                st.text_input(key="lp", label="Password")
                st.write("")
            with tab2:
                signup_username = ""
                st.header("Signup")
                st.write("")
                signup_username = st.text_input(key="su", label="Username")
                st.write("")
                st.text_input(key="sp", label="Password")
                st.write("")
            submitted = st.form_submit_button(key="register", label="Submit")
        if submitted:
            st.session_state.page = 0
            st.rerun()

    
    with col3:
        pass
