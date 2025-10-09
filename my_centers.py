import streamlit as st
import bcrypt
from supabase import create_client, Client
import random
import string
import json

def my_centers_page():
    # Initialize Supabase client
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase: Client = create_client(url, key)

    # Fetch current user by username
    user_resp = supabase.table("users").select("*").eq("username", st.session_state.username).execute()

    if not user_resp.data or len(user_resp.data) == 0:
        st.error("User not found. Please log in again.")
        return

    user = user_resp.data[0]

    # Verify password
    if not bcrypt.checkpw(st.session_state.password.encode("utf-8"), user["password"].encode("utf-8")):
        st.error("Incorrect password. Please log in again.")
        return

    # Get user center IDs (default to empty list if None)
    user_center_ids = user.get("center_ids") or []

    center_terminal = st.container()

    # Fetch all centers
    centers_resp = supabase.table("centers").select("*").execute()
    centers = centers_resp.data or []

    # -------- Join a Center --------
    with st.form("Join a center!"):
        center_password = st.text_input("Enter Center password")
        submitted = st.form_submit_button("Join Center")
        if submitted:
            if not center_password:
                st.error("Please enter a center password.")
            else:
                # Find matching center by password
                center_to_join = next(
                    (c for c in centers if bcrypt.checkpw(center_password.encode("utf-8"), c["password"].encode("utf-8"))),
                    None
                )
                if center_to_join:
                    if center_to_join["id"] not in user_center_ids:
                        user_center_ids.append(center_to_join["id"])
                        update_resp = supabase.table("users").update({"center_ids": user_center_ids}).eq("username", st.session_state.username).execute()
                        if update_resp.data:
                            st.success(f"Successfully joined center with ID: {center_to_join['id']}")
                        else:
                            st.error("Failed to join center. Please try again.")
                    else:
                        st.info("You are already a member of this center.")
                else:
                    st.error("Center not found. Please check the password and try again.")

    # -------- Create a Center --------
    with st.form("Create a center!"):
        st.write("Or create a new center!")
        new_center_password = st.text_input("Set a password for your new center", key="new_center_pw")
        new_center_name = st.text_input("Name your center (required)", key="new_center_name")
        new_description = st.text_area("Describe your center (optional)", key="new_center_desc")
        submitted = st.form_submit_button("Create Center")

        if submitted:
            password_resp = supabase.table("centers").select("password").execute()
            existing_passwords = password_resp.data or []
            password_in_use = any(
                bcrypt.checkpw(new_center_password.encode('utf-8'), c["password"].encode('utf-8'))
                for c in existing_passwords
            )
            if password_in_use:
                st.error("This password is already in use. Please choose a different password.")
            elif not new_center_password or not new_center_name:
                st.error("Please provide both a name and password for the new center.")
            else:
                # Generate random 16-character ID
                new_center_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

                # Hash the center password
                hashed_pw = bcrypt.hashpw(new_center_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

                # Insert new center with custom ID
                create_resp = supabase.table("centers").insert({
                    "id": new_center_id,
                    "name": new_center_name,
                    "password": hashed_pw,
                    "admins": [st.session_state.username],
                    "posts": [],
                    "description": new_description
                }).execute()

                if create_resp.data and len(create_resp.data) > 0:
                    # Ensure user_center_ids is a list
                    if isinstance(user_center_ids, list):
                        centers_list = user_center_ids
                    elif isinstance(user_center_ids, str):
                        try:
                            centers_list = json.loads(user_center_ids)
                            if not isinstance(centers_list, list):
                                centers_list = [centers_list]
                        except json.JSONDecodeError:
                            centers_list = [user_center_ids] if user_center_ids else []
                    else:
                        centers_list = []

                    # Append new center ID
                    centers_list.append(new_center_id)

                    # Update user's center_ids
                    update_resp = supabase.table("users").update({"center_ids": centers_list}).eq("username", st.session_state.username).execute()
                    if update_resp.data:
                        st.success(f"Center '{new_center_name}' created with ID: {new_center_id} and joined successfully!")
                    else:
                        st.error("Failed to join the newly created center. Please try again.")
                else:
                    st.error("Failed to create center. Please try again.")

    # -------- Display User Centers --------
    st.header("Your Centers")

    # Convert user_center_ids from JSON string to Python list
    if isinstance(user_center_ids, str):
        try:
            centers_list = json.loads(user_center_ids)
            if not isinstance(centers_list, list):
                centers_list = [centers_list]
        except json.JSONDecodeError:
            centers_list = []
    elif isinstance(user_center_ids, list):
        centers_list = user_center_ids
    else:
        centers_list = []

    # Build a dictionary for fast lookup of centers by ID
    centers_dict = {c["id"]: c for c in centers}

    if centers_list:
        for cid in centers_list:
            # Ensure each cid is a string and stripped
            cid_str = str(cid).strip()
            center = centers_dict.get(cid_str)
            if center:
                with st.container(border=True):
                    st.html(f"""
                            <div>
                                <h1>{center['name']}</h1>
                                <p style="background-color: #f0f0f0; border-radius: 5px; padding: 10px;">Description: {center.get('description', 'No description provided.')}</p>
                            </div>
                        """)
                    st.button("Go to Center", key=f"go_{cid_str}")
            else:
                st.write(f"- Center ID: {cid_str} (not found or deleted)")
    else:
        st.write("You haven't joined any centers yet.")

    st.write("Use the forms above to join or create a center.")