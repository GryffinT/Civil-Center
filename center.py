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
    @st.cache_data(ttl=10)
    def get_center_posts(center_id):
        resp = supabase.table("centers").select("posts").eq("id", center_id).execute()
        if resp.data:
            posts_str = resp.data[0].get("posts", "[]")
            try:
                posts_list = ast.literal_eval(posts_str)
                if not isinstance(posts_list, list):
                    posts_list = []
            except (ValueError, SyntaxError):
                posts_list = []
            return posts_list
        return []

    posts_list = get_center_posts(center_id)

    with col_main:
        st.subheader("Center Posts")
        posts_container = st.container()

        # --- Fetch posts fresh from Supabase ---
        center_posts_resp = supabase.table("centers").select("posts").eq("id", center_id).execute()
        if center_posts_resp.data:
            posts_str = center_posts_resp.data[0].get("posts", "[]")
            try:
                posts_list = ast.literal_eval(posts_str)
                if not isinstance(posts_list, list):
                    posts_list = []
            except (ValueError, SyntaxError):
                posts_list = []
        else:
            posts_list = []

        # --- Display posts ---
        if posts_list:
            for post in reversed(posts_list):  # show newest first
                title = post.get("title", "Untitled")
                name = post.get("name", "Unknown")
                content = post.get("content", "")

                with posts_container:
                    st.html(f"""
                        <div style="
                            border: 1px solid #ccc;
                            border-radius: 10px;
                            padding: 1em;
                            margin: 1em 0;
                            background-color: #fafafa;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                        ">
                            <h2 style="margin-bottom: 0.5em;">{title}</h2>
                            <h4 style="color: #666; margin-top: 0;">Posted by {name}</h4>
                            <p style="overflow-wrap: break-word; white-space: pre-wrap;">{content}</p>
                        </div>
                    """)
        else:
            st.info("No posts yet — be the first to post!")


    # ---------- Right-Side Controls ----------
    with col_controls:
        # Wrap controls in a bordered container
        with st.container(border=True):
            st.html("""
                <div>
                    <h2 style="margin-bottom: 0;">Center Controls</h2>
                    <p style="overflow-wrap: break-word; margin-top: 5px;">
                        Manage your presence in this center here.
                    </p>
                </div>
            """)

            # Buttons for leave and post
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
                    # Build the post dictionary
                    post_data = {"title": ptitle, "name": pname, "content": pcont}

                    # --- Fetch current posts from Supabase ---
                    center_posts_resp = supabase.table("centers").select("posts").eq("id", center_id).execute()
                    if center_posts_resp.data:
                        posts_str = center_posts_resp.data[0].get("posts", "[]")
                        try:
                            posts_list = ast.literal_eval(posts_str)
                            if not isinstance(posts_list, list):
                                posts_list = []
                        except (ValueError, SyntaxError):
                            posts_list = []
                    else:
                        posts_list = []

                    # --- Append new post ---
                    posts_list.append(post_data)

                    # --- Convert list back to string and update Supabase ---
                    updated_posts_str = str(posts_list)
                    supabase.table("centers").update({"posts": updated_posts_str}).eq("id", center_id).execute()

                    # --- Store in session_state for immediate display ---
                    if "posts" not in st.session_state:
                        st.session_state.posts = []
                    st.session_state.posts = posts_list  # sync session with DB

                    st.success("Post created successfully!")
                    st.rerun()

            # Open the dialog when "Make Post" is clicked
            if post_btn:
                make_post()