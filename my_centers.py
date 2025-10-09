import streamlit as st
import bcrypt
from supabase import create_client, Client

def my_centers_page():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase: Client = create_client(url, key)

    user_resp = supabase.table("users").select("center_ids").eq("password", st.session_state.password).execute()
    if user_resp.data:
        user_center_ids = user_resp.data[0]["center_ids"] or []
    else:
        user_center_ids = []
        st.error("User not found. Please log in again.")
        return

    center_terminal = st.container()
    with center_terminal:
        centers_resp = supabase.table("centers").select("*").execute()
        centers_data = centers_resp.data if centers_resp.data else []

        with st.form("join_center_form"):
            st.subheader("Join a center")
            center_password = st.text_input("Enter Center password")
            submitted_join = st.form_submit_button("Join Center")

            if submitted_join:
                center_to_join = None
                for c in centers_data:
                    if bcrypt.checkpw(center_password.encode('utf-8'), c["password"].encode('utf-8')):
                        center_to_join = c
                        break

                if center_to_join:
                    if center_to_join["id"] not in user_center_ids:
                        user_center_ids.append(center_to_join["id"])
                        update_resp = supabase.table("users").update({"center_ids": user_center_ids}).eq("password", st.session_state.password).execute()
                        if update_resp.data:
                            st.success(f"Successfully joined center with ID: {center_to_join['id']}")
                        else:
                            st.error("Failed to join center. Please try again.")
                    else:
                        st.info("You are already a member of this center.")
                else:
                    st.error("Center not found. Please check the password and try again.")

        with st.form("create_center_form"):
            st.subheader("Create a new center")
            new_center_name = st.text_input("Name your center (optional)")
            new_center_password = st.text_input("Set a password for your new center", key="new_center_pw")
            submitted_create = st.form_submit_button("Create Center")

            if submitted_create:
                if new_center_password:
                    hashed_pw = bcrypt.hashpw(new_center_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    center_data = {"password": hashed_pw}
                    if new_center_name:
                        center_data["name"] = new_center_name

                    create_resp = supabase.table("centers").insert(center_data).execute()
                    if create_resp.data:
                        new_center_id = create_resp.data[0]["id"]
                        user_center_ids.append(new_center_id)
                        update_resp = supabase.table("users").update({"center_ids": user_center_ids}).eq("password", st.session_state.password).execute()
                        if update_resp.data:
                            st.success(f"Center created with ID: {new_center_id} and joined successfully!")
                        else:
                            st.error("Failed to join the newly created center. Please try again.")
                    else:
                        st.error("Failed to create center. Please try again.")
                else:
                    st.error("Please provide a password for the new center.")

    if user_center_ids:
        st.write("Your center IDs:", user_center_ids)
    else:
        st.header("Join some centers to see them here!")

