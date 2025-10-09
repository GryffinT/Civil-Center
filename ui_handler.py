from landing import landing_page
import streamlit as st
from login import login_page
from my_centers import my_centers_page
from center import center_page
from streamlit.components.v1 import declare_component
from streamlit.components.v1 import html
from pathlib import Path
from streamlit_navigation_bar import st_navbar

if "page" not in st.session_state:
  st.session_state.page = 0
if "active_center" not in st.session_state:
  st.session_state.active_center = None
page = ""
if st.session_state.page == 0 or page == "Home":
  st.session_state.page = 0
  landing_page()
elif st.session_state.page == 1:
  login_page()
elif st.session_state.page == 2 or page == "My Centers":
  st.session_state.page = 2
  my_centers_page()
elif st.session_state.page == 3:
  center_page(st.session_state.active_center)
