from landing import landing_page
import streamlit as st
from login import login_page
from my_centers import my_centers_page

if "page" not in st.session_state:
  st.session_state.page = 0
if "active_center" not in st.session_state:
  st.session_state.active_center = None

if st.session_state.page == 0:
  landing_page()
elif st.session_state.page == 1:
  login_page()
elif st.session_state.page == 2:
  my_centers_page()
elif st.session_state.page == 3:
  st.write(f"Active Center ID: {st.session_state.active_center}")
