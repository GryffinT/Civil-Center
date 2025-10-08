from landing import landing_page
import streamlit as st
from login import login_page

if "page" not in st.session_state:
  st.session_state.page = 0

if st.session_state.page == 0:
  landing_page()
elif st.session_state.page == 1:
  login_page()
