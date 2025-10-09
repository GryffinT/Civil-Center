import streamlit as st
import bcrypt
from supabase import create_client, Client

def my_centers_page():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase: Client = create_client(url, key)

    user_resp = supabase.table("users").select("center_ids").eq("password", st.session_state.password).execute()

    if user_resp.data is not None and len(user_resp.data) > 0:
        user_center_ids = user_resp.data[0].get("center_ids") or []
    else:
        st.error(f"User not found. Please log in again. {st.session_state.password}")
        return

    center_terminal = st.container()

    with center_terminal:
        centers_resp = supabase.table("centers").select("*").execute()
        centers = centers_resp.data or []

        with st.form("Join a center!"):
            center_password = st.text_input("Enter Center password")
            submitted = st.form_submit_button("Join Center")
            if submitted:
                if not center_password:
                    st.error("Please enter a center password.")
                else:
                    center_to_join = next(
                        (c for c in centers if bcrypt.checkpw(center_password.encode('utf-8'), c["password"].encode('utf-8'))),
                        None
                    )
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

        with st.form("Create a center!"):
            st.write("Or create a new center!")
            new_center_password = st.text_input("Set a password for your new center", key="new_center_pw")
            new_center_name = st.text_input("Name your center (required)", key="new_center_name")
            submitted = st.form_submit_button("Create Center")
            if submitted:
                if not new_center_password or not new_center_name:
                    st.error("Please provide both a name and password for the new center.")
                else:
                    hashed_pw = bcrypt.hashpw(new_center_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    create_resp = supabase.table("centers").insert({
                        "name": new_center_name,
                        "password": hashed_pw,
                        "admins": [st.session_state.username],
                        "posts": []
                    }).execute()

                    if create_resp.data:
                        new_center_id = create_resp.data[0]["id"]
                        user_center_ids.append(new_center_id)
                        update_resp = supabase.table("users").update({"center_ids": user_center_ids}).eq("password", st.session_state.password).execute()
                        if update_resp.data:
                            st.success(f"Center '{new_center_name}' created with ID: {new_center_id} and joined successfully!")
                        else:
                            st.error("Failed to join the newly created center. Please try again.")
                    else:
                        st.error("Failed to create center. Please try again.")

    st.header("Your Centers")
    if user_center_ids:
        for cid in user_center_ids:
            st.write(f"- Center ID: {cid}")
    else:
        st.write("You haven’t joined any centers yet.")
