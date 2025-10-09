import streamlit as st
from supabase import create_client, Client
import bcrypt
import ast

def center_page(center_id):
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase: Client = create_client(url, key)
    
    # Fetch center details
    center_resp = supabase.table("centers").select("*").eq("id", center_id).execute()
    users_resp = supabase.table("users").select("*").eq("username", st.session_state.username).execute()
    if not center_resp.data or len(center_resp.data) == 0:
        st.error("Center not found.")
        return

    center = center_resp.data[0]

    top_box = st.container(border=True)
    with top_box:
        col1, col2, col3 = st.columns([1,3,1])

        with col1:
            st.html(f"""
                        <div style="text-align:center;">
                            <img src="https://i.postimg.cc/Y94ZzCy8/mentorship.gif" style="height:100px; width:100px;" />
                        </div>
                        """)
        with col2:
            st.html(f"""
                    <h1 style="margin-bottom: -5px;margin-top: 10px">{center.get('name', 'Unnamed Center')}</h1>
                    <p style="overflow-wrap: break-word;"><em>{center.get('description', f'The center for {center.get('name')}')}</em></p>
                    """)
        with col3:
            st.html(f"""
                    <div style="text-align:center; margin-top: 15px;">
                        <img src="https://i.postimg.cc/5yWZnMzD/members.gif" style="height:60px; width:60px;" />
                        <p>{center.get('members')} members</p>
                    </div>
                    """)
    col1, col2 = st.columns([8.5,1.5])
    with col1:
        pass
    with col2:
        container_box = st.container(border=True)
        with container_box:
            st.html("""
                    <div>
                        <h1>Center controls</h1>
                        <p style="overflow-wrap: break-word;">Manage your presence in this center here</p>
                    </div>
                    """)
            st.write("")
            leave = st.button("Leave center", use_container_width=True)
            st.write("")
            post = st.button("Make post", use_container_width=True)
            if leave:
                user_data = users_resp.data[0]  # assuming usernames are unique
                center_ids_str = user_data.get("center_ids", "[]")  # default to empty list string

                # Convert string to a Python list
                center_ids = ast.literal_eval(center_ids_str)  # safely converts '["id1","id2"]' to ["id1", "id2"]

                # Remove the center ID if it exists
                center_id_to_remove = center.get("id")
                if center_id_to_remove in center_ids:
                    center_ids.remove(center_id_to_remove)

                # Convert list back to string for storage
                new_center_ids_str = str(center_ids)

                # Update the user's row
                supabase.table("users").update({"center_ids": new_center_ids_str}).eq("username", st.session_state.username).execute()
                st.session_state.page = 2
                st.rerun()
    # Additional center functionalities can be added here