import streamlit as st
from supabase import create_client, Client
import bcrypt

def center_page(center_id):
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase: Client = create_client(url, key)
    
    # Fetch center details
    center_resp = supabase.table("centers").select("*").eq("id", center_id).execute()
    if not center_resp.data or len(center_resp.data) == 0:
        st.error("Center not found.")
        return

    center = center_resp.data[0]

    top_box = st.container(border=True)
    with top_box:
        col1, col2, col3 = st.columns([1,3,1])

        with col1:
            st.image("https://i.postimg.cc/Y94ZzCy8/mentorship.gif")
            st.html("""
                    <img style="wdith: 10px; height=10px;" src="https://i.postimg.cc/Y94ZzCy8/mentorship.gif"></img>
                    """)
        with col2:
            st.html(f"""
                    <h1>Center: {center.get('name', 'Unnamed Center')}</h1>
                    """)
        with col3:
            st.write("Hello")

    # Additional center functionalities can be added here