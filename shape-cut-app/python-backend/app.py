import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Set page config for a more modern look
st.set_page_config(page_title="Face Shape & Fashion Finder", layout="wide")

# --- Page Title and Description ---
st.title("Face Shape & Fashion Finder")
st.markdown("""
Welcome to the Face Shape & Fashion Finder! Upload a photo of yourself, and our AI will analyze your face to recommend the perfect hairstyle and dress for you.
*developed by mujahid ..bs bioinfromatics hazara uinversity mansehra ...03495474869*
""")

# --- Gemini API Configuration ---
# IMPORTANT: You must configure your own API key
# for the Gemini API.
genai.configure(api_key="AIzaSyAuxAcOoCs9243BsVujwLAKXmG9JPS92Wo")
model = genai.GenerativeModel('models/gemini-2.5-flash-image-preview')

# --- User Input: Image and Gender ---
col1, col2 = st.columns(2)

with col1:
    st.header("Upload Your Image")
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        st.image(uploaded_image, caption="Your Image", use_column_width=True)

with col2:
    st.header("Select Your Gender")
    gender = st.selectbox("I am a...", ("Woman", "Man"))

    if st.button("Get Recommendations"):
        if uploaded_image is not None:
            with st.spinner("Analyzing your image..."):
                image = Image.open(uploaded_image)

                # --- Dynamic Prompt Generation ---
                prompt = f"Analyze the face in this image and suggest a hairstyle and a dress for a {gender.lower()}."

                # --- Gemini API Call ---
                response = model.generate_content([prompt, image])

                # --- Display Recommendations ---
                st.subheader("Our Recommendations For You")
                st.markdown(response.text)
        else:
            st.error("Please upload an image first.")
