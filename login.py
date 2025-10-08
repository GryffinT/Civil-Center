import streamlit as st
from streamlit_javascript import st_javascript

def login_page(): 
    st.subheader("Javascript API call")
    st.button("test")
    if st.button:
        return_val =st_javascript("""function(response) { return (True)}""")
    
    return_value = st_javascript("""await fetch("https://reqres.in/api/products/3").then(function(response) {
        return response.json();
    }) """)
    
    st.markdown(f"Return value was: {return_value}")
    print(f"Return value was: {return_value}")
