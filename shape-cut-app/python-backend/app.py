import streamlit as st
from PIL import Image
import io
import google.generativeai as genai
from google.api_core import exceptions

# --- Page Configuration ---
st.set_page_config(
    page_title="Visionary Style AI",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Advanced CSS for "Glassmorphism" UI ---
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

    /* General Body Styles */
    body {
        font-family: 'Montserrat', sans-serif;
        color: #FFFFFF;
        background: url('https://www.transparenttextures.com/patterns/cubes.png'); /* Subtle background pattern */
        background-color: #1a1a2e; /* Dark blue-purple background */
    }

    /* Main App Container - Glassmorphism */
    .main > div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Title Style */
    h1 {
        color: #e0e0e0;
        text-align: center;
        font-weight: 700;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }

    /* Subheader Style */
    h2, h3 {
        color: #c792ea; /* Soft purple for accents */
    }

    /* Button Styles - Animated Gradient */
    .stButton > button {
        width: 100%;
        border: none;
        border-radius: 25px;
        color: #FFFFFF;
        background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888, #9a1792, #6a5acd);
        background-size: 200% 200%;
        padding: 12px 28px;
        cursor: pointer;
        font-size: 18px;
        font-weight: 700;
        transition: all 0.4s ease;
        animation: gradient 5s ease infinite;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(220, 39, 67, 0.7);
    }

    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Sidebar - Glassmorphism */
    .css-1d391kg {
        background: rgba(26, 26, 46, 0.8); /* Darker glass for sidebar */
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
    }

    /* Tabs - Glassmorphism */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: #FFFFFF;
        border: none;
    }
    .stTabs [data-baseweb="tab--selected"] {
        background: #6a5acd;
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Content ---
with st.sidebar:
    st.title("🔮 Visionary Style AI")
    st.markdown("---")
    user_api_key = st.text_input(
        "Enter your Gemini API Key:",
        type="password",
        help="Get your key from Google AI Studio."
    )
    st.markdown("---")
    st.info("Let our AI find the perfect style for you. Simply provide an image and get instant recommendations.")
    st.markdown("---")
    st.markdown("*Developed by Mujahid*")
    st.markdown("*BS Bioinformatics, Hazara University*")

# --- API Configuration ---
api_key_to_use = user_api_key if user_api_key else "AIzaSyAuxAcOoCs9243BsVujwLAKXmG9JPS92Wo"
model = None
if api_key_to_use:
    try:
        genai.configure(api_key=api_key_to_use)
        model = genai.GenerativeModel('models/gemini-2.5-flash-image-preview')
    except Exception as e:
        st.error(f"API Key Error: {e}")
        st.stop()

# --- Main App ---
st.title("AI-Powered Fashion & Style Advisor")

tab1, tab2 = st.tabs(["Get Your Style Analysis", "About the App"])

with tab1:
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.header("1. Your Image")
        uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        camera_image = st.camera_input("Or, use your camera")
        image_to_process = uploaded_image or camera_image

    with col2:
        st.header("2. Your Style Preference")
        gender = st.selectbox("Style for a...", ("Woman", "Man"), label_visibility="collapsed")

        if st.button("✨ Generate My Style ✨"):
            if not api_key_to_use:
                st.error("Please enter your Gemini API Key in the sidebar to begin.")
            elif image_to_process is None:
                st.warning("Please upload or capture an image first.")
            else:
                st.session_state.image = image_to_process
                st.session_state.gender = gender

    if 'image' in st.session_state:
        st.markdown("---")
        st.header("3. Your Personalized Results")

        result_col1, result_col2 = st.columns(2)
        with result_col1:
            st.image(st.session_state.image, caption="Your Analyzed Image", use_column_width=True)

        with result_col2:
            with st.spinner("🔮 Our AI is crafting your recommendations..."):
                try:
                    image = Image.open(st.session_state.image)
                    prompt = (f"Analyze the face for a {st.session_state.gender.lower()}. "
                              "Recommend a hairstyle and dress style. Be detailed, explaining why they suit the face shape.")

                    response = model.generate_content([prompt, image])
                    st.success("Here are your recommendations!")
                    st.markdown(response.text)

                except exceptions.ResourceExhausted:
                    st.error("API Quota Exceeded. Please try again later or use a different key.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

                # Clear session state to allow for a new run
                del st.session_state.image
                del st.session_state.gender

with tab2:
    st.header("About Visionary Style AI")
    st.markdown("""
    This application leverages Google's powerful Gemini AI to provide personalized fashion and hairstyle recommendations.
    By analyzing the unique contours and features of your face, our AI can suggest styles that are most likely to complement you.

    **How it Works:**
    1.  **Upload or Capture:** Provide an image of your face.
    2.  **Select Preference:** Choose the style you're interested in.
    3.  **AI Analysis:** The AI model processes the image to understand your facial structure.
    4.  **Get Recommendations:** Receive detailed suggestions for hairstyles and clothing.

    This tool is a demonstration of the power of generative AI in the world of fashion and personal styling.
    """)
