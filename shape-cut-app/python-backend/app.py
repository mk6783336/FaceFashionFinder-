import streamlit as st
from PIL import Image
import io
import google.generativeai as genai
from google.api_core import exceptions
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="StyleSwap AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- New Design Language CSS ---
st.markdown("""
<style>
    /* ... [CSS styles remain the same] ... */
</style>
""", unsafe_allow_html=True)


# --- Model Images Data ---
HAIRSTYLES = {
    "Woman": {
        "Long Wavy": "app/models/woman_long_wavy.jpg", "Bob Cut": "app/models/woman_bob_cut.jpg",
        "Pixie Cut": "app/models/woman_pixie_cut.jpg", "Messy Bun": "app/models/woman_messy_bun.jpg",
    },
    "Man": {
        "Crew Cut": "app/models/man_crew_cut.jpg", "Long Wavy": "app/models/man_long_wavy.jpg",
        "Buzz Cut": "app/models/man_buzz_cut.jpg", "Combover": "app/models/man_combover.jpg",
    }
}

# --- Sidebar Content ---
with st.sidebar:
    st.title("🎨 StyleSwap AI")
    st.markdown("---")
    user_api_key = st.text_input("Enter your Gemini API Key:", type="password", help="Get your key from Google AI Studio.")
    st.markdown("---")
    st.info("The future of style is here. Swap your face onto our models to see your new look in seconds.")
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
st.title("AI Face Swap & Hairstyle Advisor")

tab1, tab2 = st.tabs(["Face Swap Try-On", "How It Works"])

with tab1:
    st.header("1. Upload Your Photo")
    uploaded_image = st.file_uploader("Choose a clear, front-facing photo...", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

    if uploaded_image:
        st.image(uploaded_image, caption="Your Photo", width=200)

    st.header("2. Choose a Style")
    gender = st.radio("Show styles for a:", ("Woman", "Man"), horizontal=True)
    styles_to_show = HAIRSTYLES[gender]

    cols = st.columns(4)
    for i, (style, model_image_path) in enumerate(styles_to_show.items()):
        col = cols[i % 4]
        if os.path.exists(model_image_path):
            try:
                image = Image.open(model_image_path)
                col.image(image, use_container_width=True)
            except Exception as e:
                col.error(f"Failed to load {style}")
        else:
            col.image(Image.new('RGB', (200, 200), color = '#F0F2F6'), use_container_width=True)

        if col.button(style, key=style):
            if uploaded_image is None:
                st.warning("Please upload your photo first!")
            else:
                st.session_state.uploaded_image = uploaded_image
                st.session_state.selected_style = style
                st.session_state.selected_model = model_image_path
                if 'generated_image' in st.session_state:
                    del st.session_state.generated_image

    if 'selected_style' in st.session_state and 'generated_image' not in st.session_state:
        with st.spinner(f"🎨 Swapping your face onto the {st.session_state.selected_style} model..."):
            try:
                user_img = Image.open(st.session_state.uploaded_image)
                model_img = Image.open(st.session_state.selected_model) if os.path.exists(st.session_state.selected_model) else Image.new('RGB', (512, 512), color = 'white')
                prompt = ("Take the face from the first image and swap it onto the person in the second image. "
                          "Ensure the final image is realistic, maintaining the hairstyle and clothing of the second image.")
                response = image_gen_model.generate_content([prompt, user_img, model_img])
                generated_image_data = response.parts[0].inline_data.data
                st.session_state.generated_image = Image.open(io.BytesIO(generated_image_data))
            except exceptions.ResourceExhausted:
                st.error("API Quota Exceeded. Please try again later or use a different key.")
            except Exception as e:
                st.error(f"An error occurred during the face swap: {e}")

    if 'generated_image' in st.session_state:
        st.markdown("---")
        st.header("3. Your New Look!")
        before_col, after_col = st.columns(2)
        before_col.image(st.session_state.uploaded_image, caption="Your Photo", use_container_width=True)
        after_col.image(st.session_state.generated_image, caption=f"You with a {st.session_state.selected_style}", use_container_width=True)

with tab2:
    st.header("Welcome to the Future of Style")
    st.markdown("...") # Abridged for brevity
