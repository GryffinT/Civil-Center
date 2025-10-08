import streamlit as st

with st.container():
    st.markdown(
        '<div style="background-color: #f0f0f0; padding: 20px; border-radius: 8px;">',
        unsafe_allow_html=True
    )
    st.button("Click me")
    st.markdown('</div>', unsafe_allow_html=True)  
