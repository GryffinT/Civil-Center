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

    st.html("""
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
    """)

    # === HTML Layout ===
    st.markdown("""
    <div class="top-bar">
        <span style="padding-top: 60px;">Civil<sub>center</sub></span>
        <button id="login-btn" style="margin-left: 75%;">Login</button>
        <button id="signup-btn">Sign Up</button>
    </div>
    <div style="height: 150px;"></div>
    """, unsafe_allow_html=True)
    
    # === JavaScript bindings ===
    components.html("""
    <script>
    const login = document.getElementById("login-btn");
    const signup = document.getElementById("signup-btn");
    
    if (login) {
        login.addEventListener("click", () => {
            window.location.href = "https://docs.streamlit.io/develop/api-reference/layout/st.empty";
        });
    }
    
    if (signup) {
        signup.addEventListener("click", () => {
            window.location.href = window.location.origin + "/signup";
        });
    }
    </script>
    """, height=0)

    # Actually start putting content down here!!!

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



 
