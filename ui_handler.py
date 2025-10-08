from landing import landing_page
import streamlit as st

if "page" not in st.session_state:
  st.session_state.page = 0

if st.session_state.page == 0:
  landing_page()
elif st.session_state.page == 1:
  st.write("Login")
