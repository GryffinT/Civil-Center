from landing import landing_page
import streamlit as st
from login import login_page
from my_centers import my_centers_page
from center import center_page
from st.components.v1 import declare_component

if "page" not in st.session_state:
  st.session_state.page = 0
if "active_center" not in st.session_state:
  st.session_state.active_center = None

if st.session_state.page == 0:
  # Reuse the same component path
  black_button = declare_component("black_button", path="components/black_button")

  clicked = black_button(default=False, key="other_page_button")

  if clicked:
      st.success("Other page button clicked!")
  landing_page()
elif st.session_state.page == 1:
  login_page()
elif st.session_state.page == 2:
  my_centers_page()
elif st.session_state.page == 3:
  center_page(st.session_state.active_center)
