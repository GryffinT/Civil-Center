import streamlit as st
from PIL import Image, ImageOps, ImageDraw
import base64
from pathlib import Path
import streamlit.components.v1 as components

def landing_page():
    BASE_DIR = Path(__file__).parent
    def round_image(img_path, corner_radius, image_width=400, image_height=400):
        img = Image.open(img_path)
        img = ImageOps.fit(img, (image_width, image_height), centering=(0.5, 0.5))
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, img.size[0], img.size[1]], corner_radius, fill=255)
        img.putalpha(mask)
        return img
    st.set_page_config(page_title="Civil Center", page_icon=":guardsman:", layout="wide")

    # CSS to create frosted glass effect top bar

    # === Styles and top bar HTML ===
    st.markdown(
        """
        <style>
        body { margin: 0; }
    
        /* Frosted top bar */
        .top-bar {
          position: fixed;
          top: 0;
          left: 0;
          width: 100vw;
          height: 140px;
          display: flex;
          align-items: center;
          padding: 0 30px;
          z-index: 9999;
          background: rgba(220, 219, 218, 0.5);
          backdrop-filter: blur(10px);
          -webkit-backdrop-filter: blur(10px);
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
    
        /* Move the visible title slightly down inside the bar */
        .top-bar .title {
          font-size: 44px;
          font-weight: 700;
          color: #000;
          margin-right: auto;
          padding-top: 18px; /* nudge down */
          line-height: 1;
          display: flex;
          align-items: flex-end;
        }
        .top-bar .title sub {
          font-size: 16px;
          margin-left: 6px;
          align-self: flex-end;
        }
    
        /* Container inside the top-bar for native Streamlit widgets moved there */
        .top-bar .st-widget-container {
          display: flex;
          gap: 12px;
          align-items: center;
          height: 100%;
          margin-left: 12px;
        }
    
        /* Make Streamlit button wrappers transparent so the bar shows through */
        .top-bar .stButton > button {
          background: #000;
          color: #fff;
          border-radius: 6px;
          padding: 8px 16px;
          border: none;
          font-size: 16px;
          cursor: pointer;
        }
        .top-bar .stButton > button:hover { background: #333; }
    
        /* Ensure the moved widgets are clickable and visible */
        .top-bar * { pointer-events: auto; }
    
        /* Spacer so page content doesn't hide under the fixed bar */
        .topbar-spacer { height: 140px; }
    
        /* Responsive */
        @media (max-width: 600px) {
          .top-bar { height: 110px; padding: 0 12px; }
          .top-bar .title { font-size: 28px; padding-top: 10px; }
          .topbar-spacer { height: 110px; }
        }
        </style>
    
        <div class="top-bar" id="top-bar">
          <div class="title">Civil<sub>center</sub></div>
          <!-- placeholder container where we'll move Streamlit button nodes into -->
          <div class="st-widget-container" id="topbar-widget-container"></div>
        </div>
    
        <div class="topbar-spacer"></div>
        """,
        unsafe_allow_html=True,
    )
    
    # === Create the Streamlit buttons in the normal flow (they will be moved into the top-bar) ===
    cols = st.columns([1, 1, 8])  # space for buttons; large column keeps them left-aligned in flow
    with cols[0]:
        login_clicked = st.button("Login")
    with cols[1]:
        signup_clicked = st.button("Signup")
    
    if login_clicked:
        st.success("Login clicked (handled in Python)")
    if signup_clicked:
        st.success("Signup clicked (handled in Python)")
    
    # === JS: move the Streamlit button wrappers into the .top-bar's widget container ===
    st.markdown(
        """
        <script>
        (function() {
          const MAX_TRIES = 60;
          let tries = 0;
    
          function moveButtons() {
            tries += 1;
            const container = document.getElementById("topbar-widget-container");
            const topBar = document.getElementById("top-bar");
            if (!container || !topBar) {
              if (tries < MAX_TRIES) requestAnimationFrame(moveButtons);
              return;
            }
    
            // Find Streamlit button wrappers by data-testid
            const allButtons = Array.from(document.querySelectorAll('div[data-testid="stButton"]'));
            if (allButtons.length === 0) {
              if (tries < MAX_TRIES) requestAnimationFrame(moveButtons);
              return;
            }
    
            // Heuristic: pick the two most recently rendered buttons (the last two)
            const toMove = allButtons.slice(-2);
    
            toMove.forEach(node => {
              // Avoid moving if already moved
              if (!container.contains(node)) {
                container.appendChild(node);
              }
            });
    
            // Make sure container matches top-bar height (optional)
            container.style.height = topBar.clientHeight + "px";
          }
    
          // Wait for Streamlit to render widgets and then move them
          requestAnimationFrame(moveButtons);
          // Also try again a few times to handle streaming rendering
          setTimeout(moveButtons, 150);
          setTimeout(moveButtons, 500);
          setTimeout(moveButtons, 1200);
        })();
        </script>
        """,
        unsafe_allow_html=True,
    )
    
    # === Rest of the page content ===

    col1, col2, col3 = st.columns([5,.5,5])
    with col3:
        st.image(round_image(f"{BASE_DIR}/Media/landingpage/LandingImage1.jpg", 20, 900, 600), caption="Jose Manuel Romualdez and Dan Sullivan event - August 3rd 2019")
    with col1:
        st.html("""
        <div style="text-align: justify;">
                <h1 style="font-size: 70px; color: #000;">
                    Because 
                    <span style="
                        background: linear-gradient(to right, #4462fc 45%, #FF0000);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        display: inline-block;
                    ">
                        democracy
                    </span> 
                    isn't a shouting match.
                </h1>

               <p style="font-size: 30px; color: #000;">Don't fall to the sidelines, <strong>your voice matters</strong>, so make it heard.</p>
        </div>
                """)

    container = st.container()
    container.html("""
    <div style="background-color: #f5f5f5; padding: 50px; border-radius: 15px; margin-top: 50px;padding-bottom: 100px; margin-bottom: 50px;">

        <h2 style="font-size: 40px; color: #333; text-align: center;">Join the Conversation</h2>
        <p style="text-align: center; font-size: 20px;">Wether you're a community leader or member, Civil Center is here to help you make a difference.</p>
        <br>
        
        <style>
            .small-rect {
                flex: 1;
                background-color: #FFFFFF;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .small-rect:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            }
            .middle-rect {
                margin: 0 10px;
            }
        </style>

        <!-- Inner row containing 3 small rectangles -->
        <div style="display: flex; margin-top: 30px;">

            <!-- Left small rectangle -->
            <div class="small-rect" style="text-align: left;">
                <img src="https://i.postimg.cc/ZRZqjs3q/seminar.gif" style="width:100px; height:100px;" />
                <h2 style="color: #666;">Voice your ideas</h2>
                <p style="color: #666;">Put your ideas out there, share your thoughts through posts, if you're unsure about how they'll be received, post them anonymously!</p>
            </div>

            <!-- Middle small rectangle with 10px margin -->
            <div class="small-rect middle-rect" style="text-align: left;">
                <img src="https://i.postimg.cc/9Mt4yR83/thumbs-up-thumbs-down.gif" style="width:100px; height:100px;" />
                <h2 style="color: #666;">Discuss</h2>
                <p style="color: #666;">Engage in discussions around the ideas posted by others, providing your insights and perspectives. If you support a particular idea, let it be known by up-voting it!</p>
            </div>

            <!-- Right small rectangle -->
            <div class="small-rect" style="text-align: left;">
                <img src="https://i.postimg.cc/J48fTypq/contract.gif" style="width:100px; height:100px;" />
                <h2 style="color: #666; text-align: left;">Make changes</h2>
                <p style="color: #666; text-align: left;">The most active posts are highlighted for community leaders to see and engage with! Users can also make pledges to support specific changes they'd like to see.</p>
            </div>

        </div>

    </div>
    """)
    
    container.html("""
            <h1 style="font-size: 60px;">How to join the Civil Center community</h1>
            <ul>
                <li style="font-size: 25px; margin-bottom: 10px;">Click the "Sign Up" button at the top right corner of the page.</li>
                <li style="font-size: 25px; margin-bottom: 10px;">Fill out the registration form with your details.</li>
                <li style="font-size: 25px; margin-bottom: 10px;">Verify your email address through the link sent to your inbox.</li>
                <li style="font-size: 25px; margin-bottom: 10px;">Log in using your new credentials and start engaging with the community!</li>
            """)
    
    container.html("""
                   <div style="background-color: #f5f5f5; padding: -10px; border-radius: 15px; margin-top: 50px;padding-bottom: -10px; margin-bottom: 10px;">
                    <style>
                        .small-rect2 {
                            flex: 1;
                            padding: 20px;
                            border-radius: 10px;
                            text-align: center;
                            transition: transform 0.3s ease, box-shadow 0.3s ease;
                        }

                        .middle-rect2 {
                            margin: 0 10px;
                        }
                    </style>

                    <!-- Inner row containing 3 small rectangles -->
                    <div style="display: flex; margin-top: 30px;">

                        <!-- Left small rectangle -->
                        <div class="small-rect2" style="text-align: left;">
                            <h2 style="color: #000; text-align: left;"><strong>Civil<sub>Center</sub></strong></h2>
                            <p style="color: #666;">Share your thoughts with your communities<br> and garner change, because democracy is<br> not a shouting match.</p>
                        </div>

                        <!-- Middle small rectangle with 10px margin -->
                        <div class="small-rect2 middle-rect2" style="text-align: left;">
                            <p style="color: #000; font-size: 20px;">Product</p>
                            <button style="color: #666; border: none; background: none; cursor: pointer;" onclick="window.location.href='/changelogs'">
                                Changelogs
                            </button>
                        </div>

                        <!-- Right small rectangle -->
                        <div class="small-rect2" style="text-align: left;">
                            <p style="color: #000; font-size: 20px; text-align: left;">About the team</p>
                            <button style="color: #666; border: none; background: none; cursor: pointer;" onclick="window.location.href='/about'">
                                Learn more
                            </button>
                            <button style="color: #666; border: none; background: none; cursor: pointer;" onclick="window.location.href='https://github.com/GryffinT/Civil-Center'">
                                Github
                            </button>
                        </div>
                   </div>
                   """)



 
