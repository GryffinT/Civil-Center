import streamlit as st
import bcrypt
from supabase import create_client, Client

def my_centers_page():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase: Client = create_client(url, key)
    user_resp = supabase.table("users").select("center ids").eq("password", st.session_state.password).execute()

    if user_resp.data:
        user_center_ids = user_resp.data[0]["center ids"]
        print(user_center_ids)
    else:
        user_center_ids = None
        st.header("Join some centers to see them here!")

