import streamlit as st
from PIL import Image
import google.generativeai as genai
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Face Shape & Style Advisor",
    page_icon="✨",
    layout="centered",
)

# --- App Title and Description ---
st.title("Face Shape & Style Advisor")
st.write("Upload a photo to get personalized hairstyle and dress recommendations.")

# --- API Key Input ---
api_key = st.text_input("Enter your Gemini API Key", type="password")
if not api_key:
    st.warning("Please enter your Gemini API Key to proceed.")
    st.stop()

genai.configure(api_key=api_key)

# --- Image Upload ---
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    # --- Gender Selection ---
    gender = st.selectbox("For a Woman or a Man?", ("Woman", "Man"))

    # --- Generate Recommendations ---
    if st.button("Get Recommendations"):
        model = genai.GenerativeModel('gemini-pro-vision')
        if gender == "Woman":
            prompt = "Analyzing the face shape in the image, recommend 5 hairstyles and 5 dress styles for a woman. Provide brief descriptions for each."
        else:
            prompt = "Analyzing the face shape in the image, recommend 5 hairstyles and 5 suit styles for a man. Provide brief descriptions for each."

        with st.spinner("Analyzing and generating recommendations..."):
            response = model.generate_content([prompt, image])
            st.markdown(response.text)

st.markdown("---")
st.write("Developed by mujahid ..bs bioinfromatics hazara uinversity mansehra ...03495474869")
