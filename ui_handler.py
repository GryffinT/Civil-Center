from landing import landing_page
import streamlit as st
from login import login_page
from my_centers import my_centers_page
from center import center_page
from streamlit.components.v1 import declare_component
from streamlit.components.v1 import html
from pathlib import Path


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
  if "button_clicked" not in st.session_state:
      st.session_state.button_clicked = False

  # HTML + JS
  html_code = """
  <style>
  button {
    background-color: black;
    color: white;
    border: none;
    padding: 14px 28px;
    border-radius: 8px;
    font-size: 18px;
    cursor: pointer;
    transition: 0.25s;
  }
  button:hover {
    background-color: #333;
    transform: scale(1.05);
  }
  </style>

  <button id="my-button">Click Me</button>

  <script>
  const btn = document.getElementById("my-button");

  // When the button is clicked, send a message to Streamlit
  btn.addEventListener("click", () => {
      window.parent.postMessage({isClicked: true}, "*");
  });
  </script>
  """

  # Render HTML
  html(html_code, height=100)

  # Listen for messages from JS
  import streamlit.components.v1 as components

  components.html(
      """
      <script>
      window.addEventListener("message", (event) => {
          if (event.data.isClicked) {
              window.parent.postMessage({clicked: true}, "*");
          }
      });
      </script>
      """,
      height=0,
  )

  # Use Streamlit session state to handle the click
  if st.session_state.button_clicked:
      st.success("Button was clicked!")
  else:
      # Detect the click
      js_code = """
      <script>
      window.addEventListener("message", (event) => {
          if (event.data.isClicked) {
              fetch("/_st_session_state_button", {method: "POST"})
          }
      });
      </script>
      """
      html(js_code, height=0)
  center_page(st.session_state.active_center)
