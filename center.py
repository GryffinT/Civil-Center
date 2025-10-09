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

    st.title(f"Center: {center.get('name', 'Unnamed Center')}")
    st.write(f"Description: {center.get('description', 'No description provided.')}")
    st.write(f"Center ID: {center_id}")

    # Additional center functionalities can be added here