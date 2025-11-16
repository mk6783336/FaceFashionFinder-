import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
from google.api_core import exceptions

# --- Page Configuration ---
st.set_page_config(
    page_title="Face & Fashion AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for a Modern UI/UX ---
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* General Body Styles */
    body {
        font-family: 'Roboto', sans-serif;
        color: #E0E0E0; /* Light grey text */
        background-color: #121212; /* Dark background */
    }

    /* Main App Container */
    .main > div {
        background-color: #1E1E1E;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Title Style */
    h1 {
        color: #FFFFFF;
        text-align: center;
        font-weight: 700;
    }

    /* Subheader Style */
    h2, h3 {
        color: #BB86FC; /* A vibrant accent color */
    }

    /* Button Styles */
    .stButton > button {
        width: 100%;
        border: 2px solid #BB86FC;
        border-radius: 25px;
        color: #FFFFFF;
        background-color: transparent;
        padding: 10px 24px;
        cursor: pointer;
        font-size: 18px;
        font-weight: 700;
        transition: all 0.3s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #BB86FC;
        color: #121212;
        box-shadow: 0 0 15px #BB86FC;
    }

    /* File Uploader & Camera Input Style */
    .stFileUploader, .stCameraInput {
        border: 2px dashed #3A3A3A;
        background-color: #2C2C2C;
        padding: 1rem;
        border-radius: 10px;
    }

    /* Sidebar Styles */
    .css-1d391kg {
        background-color: #1E1E1E;
    }

    /* Card for output */
    .output-card {
        background-color: #2C2C2C;
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 2rem;
        border-left: 5px solid #BB86FC;
    }

</style>
""", unsafe_allow_html=True)


# --- Gemini API Configuration ---
try:
    genai.configure(api_key="AIzaSyAuxAcOoCs9243BsVujwLAKXmG9JPS92Wo")
    model = genai.GenerativeModel('models/gemini-2.5-flash-image-preview')
except Exception as e:
    st.error(f"Failed to configure Gemini API: {e}")
    st.stop()


# --- Sidebar Content ---
with st.sidebar:
    st.title("✨ Face & Fashion AI")
    st.markdown("---")
    st.info("Upload an image or use your camera to get personalized hairstyle and dress recommendations from our AI.")
    st.markdown("---")
    st.markdown("*Developed by Mujahid*")
    st.markdown("*BS Bioinformatics, Hazara University*")


# --- Main Application ---
st.title("Face Shape & Fashion Recommender")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.header("1. Provide Your Image")
    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    camera_image = st.camera_input("Or, use your camera")

    image_to_process = uploaded_image if uploaded_image is not None else camera_image

with col2:
    st.header("2. Select Your Style")
    gender = st.selectbox("I'm looking for a style for a...", ("Woman", "Man"), label_visibility="collapsed")

    get_recs_button = st.button("Get Recommendations!")


# --- Processing and Output ---
if get_recs_button:
    if image_to_process is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.image(image_to_process, caption="Your Image", use_column_width=True)

        with col2:
            with st.spinner("🤖 AI is analyzing your image..."):
                try:
                    image = Image.open(image_to_process)
                    prompt = (f"Analyze the face in this image for a {gender.lower()}. "
                              "Provide a recommended hairstyle and a recommended dress style. "
                              "Be detailed and explain why these recommendations suit the face shape.")

                    response = model.generate_content([prompt, image])

                    st.markdown("<div class='output-card'><h3>AI Recommendations</h3></div>", unsafe_allow_html=True)
                    st.markdown(response.text)

                except exceptions.ResourceExhausted:
                    st.error("Whoops! The AI is a bit tired right now (API quota exceeded). Please try again later.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please upload an image or take a picture first!")
