from landing import landing_page
import streamlit as st
from login import login_page
from my_centers import my_centers_page
from center import center_page
from pathlib import Path
import streamlit.components.v1 as components

# --- Initialize session state ---
if "page" not in st.session_state:
    st.session_state.page = 0
if "active_center" not in st.session_state:
    st.session_state.active_center = None
if "semantic_post_content" not in st.session_state:
    st.session_state.semantic_post_content = []

page = ""

# --- Function to reset scroll ---
def scroll_to_top():
    components.html("""
        <script>
        window.scrollTo(0, 0);
        </script>
    """, height=0)

# --- Page navigation ---
if st.session_state.page == 0 or page == "Home":
    st.session_state.page = 0
    scroll_to_top()  # reset scroll
    landing_page()
elif st.session_state.page == 1:
    scroll_to_top()
    login_page()
    scroll_to_top()
elif st.session_state.page == 2 or page == "My Centers":
    st.session_state.page = 2
    scroll_to_top()
    my_centers_page()
elif st.session_state.page == 3:
    scroll_to_top()
    center_page(st.session_state.active_center)

