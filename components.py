from st.components.v1 import declare_component
import streamlit as st
from st.components.v1 import html

declare_component("frosted_top_bar", path="components")

# === Styles ===
html("""
<style>
.css-18e3th9 {
    padding: 0 !important;
    margin: 0 !important;
}

body {
    margin: 0;
}

/* Full-width frosted top bar */
.top-bar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 150px;
    display: flex;
    align-items: center;
    padding-left: 30px;
    z-index: 9999;

    background: rgba(220, 219, 218, 0.5);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* Text inside the bar */
.top-bar span {
    font-size: 50px;
    font-weight: bold;
    color: black;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    background: transparent !important;
}

/* Buttons */
.top-bar button {
    margin-top: 60px;
    margin-right: 30px;
    padding: 10px 20px;
    font-size: 20px;
    background-color: #000;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: 0.2s;
}

.top-bar button:hover {
    background-color: #333;
}

/* Transparent Streamlit boxes */
[data-testid="stTextInput"] > div:first-child, 
[data-testid="stTextArea"] > div:first-child,
.css-1adrfps {
    background-color: transparent !important;
    box-shadow: none !important;
}
</style>
""")

# === HTML Layout ===
html("""
<div class="top-bar">
    <span style="padding-top: 60px;">Civil<sub>Center</sub></span>
</div>
<div style="height: 150px;"></div>
""")
# === End Styles ===