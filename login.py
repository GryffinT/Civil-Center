import streamlit as st
from streamlit_javascript import st_javascript

if "page" not in st.session_state:
    st.session_state.page = 1

def login_page(): 
    with st.form("my_form"):
        tab1, tab2 = st.tabs(["Login", "Signup"])
        
        with tab1:
            st.header("Login")
            st.text_input("Username")
            st.text_input("Password")
        with tab2:
            st.header("Signup")
            st.text_input("Username")
            st.text_input("Password")
        submitted = st.form_submit_button()
    if submitted:
        st.session_state.page = 0
        st.rerun()
