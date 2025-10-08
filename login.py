import streamlit as st
from streamlit_javascript import st_javascript

if "page" not in st.session_state:
    st.session_state.page = 1

def login_page(): 
    with st.form("my_form"):
        tab1, tab2 = st.tabs(["Cat", "Dog"])
        
        with tab1:
            st.header("Login")
        with tab2:
            st.header("Signup")
    if submitted:
        st.session_state.page = 0
