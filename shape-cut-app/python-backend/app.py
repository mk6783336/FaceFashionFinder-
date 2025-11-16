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

# --- Hairstyle Data ---
HAIRSTYLES = {
    "Woman": ["Bob Cut", "Long Wavy", "Pixie Cut", "Curtain Bangs", "Messy Bun", "Two Braids", "Afro", "Short Curly"],
    "Man": ["Buzz Cut", "Crew Cut", "Combover", "Long Wavy", "Curtain", "Bowl Cut", "Bald", "Short Curly"]
}

# --- Advanced CSS for "Glassmorphism" UI ---
st.markdown("""
<style>
    /* ... [CSS styles remain the same] ... */
</style>
""", unsafe_allow_html=True)

# --- Sidebar Content ---
with st.sidebar:
    st.title("🔮 Visionary Style AI")
    st.markdown("---")
    user_api_key = st.text_input("Enter your Gemini API Key:", type="password", help="Get your key from Google AI Studio.")
    st.markdown("---")
    st.info("Let our AI find the perfect style for you. Simply provide an image and get instant recommendations.")
    st.markdown("---")
    st.markdown("*Developed by Mujahid*")
    st.markdown("*BS Bioinformatics, Hazara University*")

# --- API Configuration ---
api_key_to_use = user_api_key if user_api_key else "AIzaSyAuxAcOoCs9243BsVujwLAKXmG9JPS92Wo"
image_gen_model = None
if api_key_to_use:
    try:
        genai.configure(api_key=api_key_to_use)
        image_gen_model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
    except Exception as e:
        st.error(f"API Key Error: {e}")
        st.stop()

# --- Main App ---
st.title("AI Virtual Hairstyle Try-On")

tab1, tab2 = st.tabs(["Virtual Try-On", "About the App"])

with tab1:
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.header("1. Your Image")
        uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        camera_image = st.camera_input("Or, use your camera")
        image_to_process = uploaded_image or camera_image

    with col2:
        st.header("2. Your Style Preference")
        gender = st.radio("Style for a...", ("Woman", "Man"), horizontal=True, label_visibility="collapsed")

    st.header("3. Choose a Hairstyle")

    hairstyles_to_show = HAIRSTYLES[gender]

    cols = st.columns(4)
    for i, style in enumerate(hairstyles_to_show):
        if cols[i % 4].button(style, key=style):
            if not api_key_to_use:
                st.error("Please enter your Gemini API Key in the sidebar to begin.")
            elif image_to_process is None:
                st.warning("Please upload or capture an image first.")
            else:
                st.session_state.image_to_process = image_to_process
                st.session_state.selected_style = style
                if 'generated_image' in st.session_state:
                    del st.session_state.generated_image

    if 'image_to_process' in st.session_state and 'selected_style' in st.session_state and 'generated_image' not in st.session_state:
        with st.spinner(f"🔮 AI is generating your new look with a {st.session_state.selected_style}..."):
            try:
                input_image = Image.open(st.session_state.image_to_process)
                prompt = f"Edit this person's hairstyle to be a {st.session_state.selected_style}. Do not change their face or the background."
                response = image_gen_model.generate_content([prompt, input_image])
                generated_image_data = response.parts[0].inline_data.data
                st.session_state.generated_image = Image.open(io.BytesIO(generated_image_data))
            except exceptions.ResourceExhausted:
                st.error("API Quota Exceeded. Please try again later or use a different key.")
            except Exception as e:
                st.error(f"An error occurred during image generation: {e}")

    if 'generated_image' in st.session_state:
        st.markdown("---")
        st.header("4. Your Transformation!")

        before_col, after_col = st.columns(2)
        with before_col:
            st.image(st.session_state.image_to_process, caption="Before", use_column_width=True)
        with after_col:
            st.image(st.session_state.generated_image, caption="After", use_column_width=True)

with tab2:
    st.header("About Visionary Style AI")
    st.markdown("This application uses generative AI to provide a virtual hairstyle try-on experience.")
