import streamlit as st
import bcrypt
from supabase import create_client, Client

def my_centers_page():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase: Client = create_client(url, key)
    user_resp = supabase.table("users").select("center_ids").eq("password", st.session_state.password).execute()
    center_terminal = st.container(border=True)
    with center_terminal:
        centers = supabase.table("centers").select("password").execute()
        with st.form("Join a center!"):
            center_password = st.text_input("Enter Center password")
            submitted = st.form_submit_button("Join Center")
            if submitted:
                if centers.data:
                    center_to_join = centers.data[center_password]
                    if center_to_join:
                        if user_resp.data:
                            user_center_ids = user_resp.data[0]["center_ids"]
                            if center_to_join["id"] not in user_center_ids:
                                user_center_ids.append(center_to_join["id"])
                                update_resp = supabase.table("users").update({"center_ids": user_center_ids}).eq("password", st.session_state.password).execute()
                                if update_resp.status_code == 200:
                                    st.success(f"Successfully joined center with ID: {center_to_join['id']}")
                                else:
                                    st.error("Failed to join center. Please try again.")
                            else:
                                st.info("You are already a member of this center.")
                        else:
                            st.error("User not found. Please log in again.")
                    else:
                        st.error("Center not found. Please check the password and try again.")
    if user_resp.data:
        user_center_ids = user_resp.data[0]["center_ids"]
        print(user_center_ids)
    else:
        user_center_ids = None
        st.header("Join some centers to see them here!")

