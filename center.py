import streamlit as st
from supabase import create_client, Client
import ast
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity

def center_page(center_id):
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    def embed_text(text):
        return encoder.encode(text, convert_to_tensor=True)
    # === Styles ===
    st.markdown("""
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
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
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
    """, unsafe_allow_html=True)
    
    # === HTML Layout ===
    st.markdown("""
    <div class="top-bar">
        <span style="padding-top: 60px;">Civil<sub>Center</sub></span>
    </div>
    <div style="height: 150px; margin-bottom:-10px;"></div>
    """, unsafe_allow_html=True)
    
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    supabase: Client = create_client(url, key)
    st.html("""
            <br style="margin-bottom: -5px;">
            """)

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
                <div style="text-align:left;">
                    <img src="https://i.postimg.cc/Y94ZzCy8/mentorship.gif" style="height:200px; width:200px;" />
                </div>
            """)
        with col2:
            st.html(f"""
                    <div text-align: left;>
                        <h1 style="margin-bottom: -5px;margin-top: 10px; font-size: 60;">{center.get('name', 'Unnamed Center')}</h1>
                        <p style="overflow-wrap: break-word; font-size: 50;"><em>{center.get('description', f'The center for {center.get('name')}')}</em></p>
                    </div>
            """)
        with col3:
            st.html(f"""
                <div style="text-align:center; margin-top: 0 auto;">
                    <img src="https://i.postimg.cc/5yWZnMzD/members.gif" style="height:60px; width:60px;" />
                    <p style="font-size": 32;>{center.get('members')} members</p>
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
            if "semantic_post_content" not in st.session_state:
                st.session_state.semantic_post_content = []
            for post in reversed(posts_list):
                list_title = post.get("title", "Untitled")
                list_content = post.get("content", "")
                st.session_state.semantic_post_content.append(list_content)

            for post in reversed(posts_list):  # show newest first
                title = post.get("title", "Untitled")
                name = post.get("name", "Unknown")
                content = post.get("content", "")
                bad = post.get("tags", "")
                st.write(len(st.session_state.semantic_post_content))
                st.write(st.session_state.semantic_post_content)
                for entry in range(len(st.session_state.semantic_post_content)):
                    similarity = util.cos_sim(embed_text(content), embed_text(st.session_state.semantic_post_content[entry])).item()
                    st.write(similarity)
                    

                with posts_container:
                    col1, col2 = st.columns([9,1])
                    badge_map = {
                        0: "Help",
                        1: "Suggestion",
                        2: "Problem",
                    }
                    color_map = {
                        0: ["blue", "#89CFF0"],
                        1: ["#32fa8f", "#016e3d"],
                        2: ["red", "#6e0101"]
                    }
                    if bad in [0,1,2]:
                        st.html(
                            f"""
                            <div style="
                                border: 1px solid #ccc;
                                border-radius: 10px;
                                padding: 1em;
                                margin: 1em 0;
                                background-color: #fafafa;
                                box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                                
                                <h2 style="margin-bottom: 0.5em;">{title}</h2>
                                <h4 style="color: #666; margin-top: 0;">Posted by {name}</h4>
                                <p style="overflow-wrap: break-word; white-space: pre-wrap;">{content}</p>
                                <span style='display: inline-block; color: {color_map[bad][0]}; background: {color_map[bad][1]}; backdrop-filer: blur(5px); -webkit-backdrop-filter: blur(5px); border-radius: 5px; padding: 0.2em 0.6em; font-size: 0.9em;'>
                                    {badge_map[bad]}
                                </span>
                            </div>
                            """)
                    else:
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
            back = st.button("Back", use_container_width=True)

            if back:
                st.session_state.page = 2
                st.rerun()
            
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
                            try:
                                rpc_resp = supabase.rpc("decrement_members", {"center_id": center_id_to_remove}).execute()
                            except Exception as rpc_err:
                                st.write(f"Couldn't increment center member count (RPC error): {rpc_err}")
                            #supabase.table("centers").update({"members": new_member_count}).eq("id", center_id_to_remove).execute()

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
                option_map = {
                    0: "Help",
                    1: "Suggestion",
                    2: "Problem",
                }
                selection = st.pills(
                    "Tags",
                    options=option_map.keys(),
                    format_func=lambda option: option_map[option],
                    selection_mode="single",
                )
                if st.button("Post"):
                    # Build the post dictionary
                    post_data = {"title": ptitle, "name": pname, "content": pcont, "tags": selection}

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
