import streamlit as st
from streamlit.components.v1 import html
import bcrypt
from supabase import create_client, Client
import random
import string
import json
import ast
from typing import Any, List, Dict

# ---------------- Helper functions ----------------
def parse_center_ids(value: Any) -> List[str]:
    """
    Parse center_ids stored as a Python list, a JSON string '["id"]',
    or a Python literal string "['id']". Return a clean list of strings.
    """
    if value is None:
        return []
    # If it's already a list, return a copy of stringified items
    if isinstance(value, list):
        return [str(x).strip() for x in value]

    # Try JSON parse first (most likely)
    if isinstance(value, str):
        value_str = value.strip()
        # empty string
        if value_str == "":
            return []
        # Try JSON
        try:
            parsed = json.loads(value_str)
            if isinstance(parsed, list):
                return [str(x).strip() for x in parsed]
            return [str(parsed).strip()]
        except json.JSONDecodeError:
            # Try safe literal eval (e.g. "['id']" or "['id','id2']")
            try:
                parsed = ast.literal_eval(value_str)
                if isinstance(parsed, list):
                    return [str(x).strip() for x in parsed]
                return [str(parsed).strip()]
            except (ValueError, SyntaxError):
                # Fall back: single string value
                return [value_str]

    # Any other type: coerce to string
    return [str(value).strip()]


def stringify_center_ids(lst: List[str]) -> str:
    """Convert a list of center ids into a string form to store in DB."""
    # store as a Python-like list string (keeps your previous format)
    return str([str(x) for x in lst])


def display_center_card(center: Dict[str, Any], key_suffix: Any = None):
    """
    Display a styled center card with a "Go to Center" button.
    key_suffix used to create unique button keys.
    """
    key_suffix = key_suffix if key_suffix is not None else center.get("id", "")
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="
                padding: 15px; 
                border-radius: 10px; 
                background-color: #fafafa; 
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                margin-bottom: 10px;
            ">
                <h2 style="margin-bottom: 10px;">{center.get('name', 'Unnamed Center')}</h2>
                <p style="background-color: #f0f0f0; border-radius: 5px; padding: 10px;">
                    Description: {center.get('description', 'No description provided.')}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Go to Center", key=f"go_{key_suffix}", use_container_width=True):
            st.session_state.active_center = center.get("id")
            st.session_state.page = 3
            st.rerun()


# ---------------- Main page function ----------------
def my_centers_page():
    # === Styles ===
    st.markdown(
        """
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
    """,
        unsafe_allow_html=True,
    )

    # === HTML Layout ===
    st.markdown(
        """
    <div class="top-bar">
        <span style="padding-top: 60px;">Civil<sub>Center</sub></span>
    </div>
    <div style="height: 150px;"></div>
    """,
        unsafe_allow_html=True,
    )
    # === End Styles ===

    # Initialize Supabase client
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase: Client = create_client(url, key)

    # Check session_state for required fields
    if "username" not in st.session_state or "password" not in st.session_state:
        st.error("Missing session info. Please log in.")
        return

    # Fetch current user by username
    user_resp = supabase.table("users").select("*").eq("username", st.session_state.username).execute()

    if not user_resp or not getattr(user_resp, "data", None) or len(user_resp.data) == 0:
        st.error("User not found. Please log in again.")
        return

    user = user_resp.data[0]

    # Verify password (user["password"] should be the hashed password string)
    try:
        if not bcrypt.checkpw(st.session_state.password.encode("utf-8"), user["password"].encode("utf-8")):
            st.error("Incorrect password. Please log in again.")
            return
    except Exception as e:
        st.error("Error verifying password.")
        st.exception(e)
        return

    # Parse user's center IDs into a list
    user_center_ids = parse_center_ids(user.get("center_ids"))

    # Fetch all centers once
    centers_resp = supabase.table("centers").select("*").execute()
    centers = centers_resp.data or []

    # Build a dictionary for fast lookup of centers by ID
    centers_dict = {str(c.get("id")): c for c in centers}

    # -------- Join a Center --------
    with st.form("join_center_form"):
        center_password = st.text_input("Enter Center password", type="password")
        submitted = st.form_submit_button("Join Center")
        if submitted:
            if not center_password:
                st.error("Please enter a center password.")
            else:
                # Find matching center by password
                center_to_join = next(
                    (
                        c
                        for c in centers
                        if c.get("password")
                        and bcrypt.checkpw(center_password.encode("utf-8"), c["password"].encode("utf-8"))
                    ),
                    None,
                )

                if not center_to_join:
                    st.error("Center not found. Please check the password and try again.")
                else:
                    center_id = str(center_to_join["id"]).strip()
                    # Re-parse in case user_center_ids changed elsewhere
                    user_center_ids = parse_center_ids(user.get("center_ids"))

                    if center_id in user_center_ids:
                        st.info("You are already a member of this center.")
                    else:
                        # Append and persist
                        user_center_ids.append(center_id)
                        updated_center_ids_str = stringify_center_ids(user_center_ids)

                        # Update user's center_ids in Supabase
                        update_resp = supabase.table("users").update({"center_ids": updated_center_ids_str}).eq(
                            "username", st.session_state.username
                        ).execute()

                        # Call RPC to increment members count (gracefully handle errors)
                        try:
                            rpc_resp = supabase.rpc("increment_members", {"center_id": center_id}).execute()
                        except Exception as rpc_err:
                            rpc_resp = None
                            st.warning("Couldn't increment center member count (RPC error).")

                        if update_resp and getattr(update_resp, "data", None):
                            st.success(f"Successfully joined center with ID: {center_id}")
                            st.rerun()
                        else:
                            st.error("Failed to join center. Please try again.")

    # -------- Create a Center --------
    with st.form("create_center_form"):
        st.write("Or create a new center!")
        new_center_password = st.text_input("Set a password for your new center", key="new_center_pw", type="password")
        new_center_name = st.text_input("Name your center (required)", key="new_center_name")
        new_description = st.text_area("Describe your center (optional)", key="new_center_desc")
        submitted = st.form_submit_button("Create Center")

        if submitted:
            # Get existing hashed passwords to avoid duplicates
            password_resp = supabase.table("centers").select("password").execute()
            existing_passwords = password_resp.data or []

            password_in_use = any(
                bcrypt.checkpw(new_center_password.encode("utf-8"), c["password"].encode("utf-8"))
                for c in existing_passwords
            ) if new_center_password else False

            if password_in_use:
                st.error("This password is already in use. Please choose a different password.")
            elif not new_center_password or not new_center_name:
                st.error("Please provide both a name and password for the new center.")
            else:
                # Generate random 16-character ID
                new_center_id = "".join(random.choices(string.ascii_letters + string.digits, k=16))

                # Hash the center password
                hashed_pw = bcrypt.hashpw(new_center_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

                # Insert new center with custom ID
                create_resp = supabase.table("centers").insert(
                    {
                        "id": new_center_id,
                        "name": new_center_name,
                        "password": hashed_pw,
                        "admins": [st.session_state.username],
                        "posts": [],
                        "description": new_description,
                        "members": 1,
                    }
                ).execute()

                if create_resp and getattr(create_resp, "data", None) and len(create_resp.data) > 0:
                    # Parse stored user_center_ids afresh
                    current_user_centers = parse_center_ids(user.get("center_ids"))

                    if new_center_id not in current_user_centers:
                        current_user_centers.append(new_center_id)

                    new_center_ids_str = stringify_center_ids(current_user_centers)

                    update_resp = supabase.table("users").update({"center_ids": new_center_ids_str}).eq(
                        "username", st.session_state.username
                    ).execute()

                    if update_resp and getattr(update_resp, "data", None):
                        st.success(f"Successfully created and joined center '{new_center_name}' with ID: {new_center_id}")
                        st.rerun()
                    else:
                        st.error("Failed to update your profile with the new center. Please try again.")
                else:
                    st.error("Failed to create center. Please try again.")

    # -------- Display User Centers --------
    st.header("Your Centers")

    # Re-parse user_center_ids (in case changed)
    user_center_ids = parse_center_ids(user.get("center_ids"))

    if user_center_ids:
        for i, cid in enumerate(user_center_ids):
            cid_str = str(cid).strip()
            center = centers_dict.get(cid_str)
            if center:
                display_center_card(center, key_suffix=i)
            else:
                st.write(f"- Center ID: {cid_str} (not found or deleted)")
    else:
        st.write("You haven't joined any centers yet.")

    st.write("Use the forms above to join or create a center.")
