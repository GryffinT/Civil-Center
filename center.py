import streamlit as st
from supabase import create_client, Client
import ast

def center_page(center_id):
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase: Client = create_client(url, key)

    # Fetch center details
    center_resp = supabase.table("centers").select("*").eq("id", center_id).execute()
    users_resp = supabase.table("users").select("*").eq("username", st.session_state.username).execute()

    if not center_resp.data:
        st.error("Center not found.")
        return

    center = center_resp.data[0]

    # =========================
    # Top Section (Header)
    # =========================
    top_box = st.container(border=True)
    with top_box:
        col1, col2, col3 = st.columns([1,3,1])

        with col1:
            st.html("""
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

    # =========================
    # Main Layout: Posts + Controls
    # =========================
    col_main, col_controls = st.columns([8.5, 1.5])

    # ---------- Main Posts Section ----------
    with col_main:
        st.subheader("Center Posts")
        posts_container = st.container()

        # Display all posts stored in session_state
        if "posts" in st.session_state and st.session_state.posts:
            for post in st.session_state.posts:
                with posts_container:
                    st.html(f"""
                        <div style="border: 1px solid #ccc; border-radius: 10px; padding: 1em; margin: 1em 0;">
                            <h2>{post['title']}</h2>
                            <h4>Posted by {post['name']}</h4>
                            <p style="overflow-wrap: break-word;">{post['content']}</p>
                        </div>
                    """)
        else:
            st.info("No posts yet — be the first to post!")

    # ---------- Right-Side Controls ----------
    with col_controls:
        st.html("""
            <div>
                <h2>Center Controls</h2>
                <p style="overflow-wrap: break-word;">Manage your presence in this center here</p>
            </div>
        """)

        leave = st.button("Leave Center", use_container_width=True)
        post_btn = st.button("Make Post", use_container_width=True)

        # Handle leaving
        if leave:
            user_data = users_resp.data[0]
            center_ids_str = user_data.get("center_ids", "[]")

            try:
                center_ids = ast.literal_eval(center_ids_str)
                if not isinstance(center_ids, list):
                    center_ids = []
            except (ValueError, SyntaxError):
                center_ids = []

            center_id_to_remove = center.get("id")
            if center_id_to_remove in center_ids:
                center_ids.remove(center_id_to_remove)
                new_center_ids_str = str(center_ids)

                supabase.table("users").update({"center_ids": new_center_ids_str}).eq(
                    "username", st.session_state.username
                ).execute()

                # Update or delete the center
                center_resp = supabase.table("centers").select("members").eq("id", center_id_to_remove).execute()
                if center_resp.data:
                    current_members = center_resp.data[0].get("members", 1)
                    new_member_count = max(current_members - 1, 0)

                    if new_member_count == 0:
                        supabase.table("centers").delete().eq("id", center_id_to_remove).execute()
                        st.info(f"The center '{center.get('name', center_id_to_remove)}' has been deleted (no remaining members).")
                    else:
                        supabase.table("centers").update({"members": new_member_count}).eq("id", center_id_to_remove).execute()

                st.success(f"You have left the center '{center.get('name', center_id_to_remove)}'.")
                st.session_state.page = 2
                st.rerun()
            else:
                st.warning("You are not a member of this center.")

        # ---------- Post Dialog ----------
        @st.dialog("What's on your mind?")
        def make_post():
            ptitle = st.text_input("Title")
            pname = "Anonymous" if st.toggle("Post anonymously") else st.session_state.username
            pcont = st.text_area("Content")

            if st.button("Post"):
                if "posts" not in st.session_state:
                    st.session_state.posts = []
                st.session_state.posts.append({
                    "title": ptitle,
                    "name": pname,
                    "content": pcont
                })
                st.rerun()

        # Open the dialog
        if post_btn:
            make_post()
