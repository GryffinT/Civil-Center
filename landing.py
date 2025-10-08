import streamlit as st
from PIL import Image, ImageOps, ImageDraw
from streamlit_drawable_canvas import st_canvas
import base64

def landing_page():
    def round_image(img_path, corner_radius, image_width=400, image_height=400):
        img = Image.open(img_path)
        img = ImageOps.fit(img, (image_width, image_height), centering=(0.5, 0.5))
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, img.size[0], img.size[1]], corner_radius, fill=255)
        img.putalpha(mask)
        return img
    st.set_page_config(page_title="Civil Center", page_icon=":guardsman:", layout="wide")


    # Background rectangles
    def make_fullwidth_rectangle(height, color="#f0f2f6"):
        st.markdown(
            f"""
            <div style="
                width: 100vw;              /* full viewport width */
                margin-left: calc(-50vw + 50%);
                height: {height}px;
                background-color: {color};
            "><p></div>
            """,
            unsafe_allow_html=True
        )


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
        height: 150px;          /* taller bar */
        display: flex;
        align-items: center;     /* vertical center */
        padding-left: 30px;
        z-index: 9999;

        /* Frosted glass effect */
        background: rgba(255, 255, 255, 0.5); 
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
        background: transparent !important;  /* ensure no background */
    }

    /* Make Streamlit text_input and markdown boxes transparent over top bar */
    [data-testid="stTextInput"] > div:first-child, 
    [data-testid="stTextArea"] > div:first-child,
    .css-1adrfps {  /* general container class for text boxes */
        background-color: transparent !important;
        box-shadow: none !important;
    }
    """)

    # Render the frosted top bar with text
    st.html("""
    <div class="top-bar">
        <span style="padding-top: 60px; background: transparent;">Civil<sub>center</sub></span>
    </div>
    """)

    # Spacer so content isn't hidden under fixed bar
    st.html("<div style='height: 150px;'></div>")

    # Actually start putting content down here!!!

    col1, col2, col3 = st.columns([5,.5,5])
    with col3:
        st.image(round_image("./Media/landingpage/landingimage1.jpg", 20, 900, 600), caption="Jose Manuel Romualdez and Dan Sullivan event - August 3rd 2019")
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
        
    file_path = "./Media/landingpage/seminar.gif"
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()

    container = st.container()
    container.html("""
    <div style="background-color: #f5f5f5; padding: 50px; border-radius: 15px; margin-top: 50px;">

        <h2 style="font-size: 40px; color: #333; text-align: center;">Join the Conversation</h2>
        
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
                <img src="data:image/gif;base64,{b64}" style="width:100px; height:100px;" />
                <p style="color: #666;">Voice your ideas</p>
            </div>

            <!-- Middle small rectangle with 10px margin -->
            <div class="small-rect middle-rect">
                <p style="color: #666;">I rise in...</p>
            </div>

            <!-- Right small rectangle -->
            <div class="small-rect">
                <h2 style="color: #666; text-align: left;">And the motion...</h2>
            </div>

        </div>

    </div>
    """)



 