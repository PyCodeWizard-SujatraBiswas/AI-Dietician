from dotenv import load_dotenv

load_dotenv()  # Load all the environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro Vision
model = genai.GenerativeModel('gemini-pro-vision')


def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# Initialize streamlit app
st.set_page_config(page_title="AI Dietician")

st.header("Ask your AI Dietician")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an Image of the Invoice....", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Answer")

input_prompt = """
You are an expert AI Dietician API designed to analyze a user's medical report and craft 
a personalized diet chart for a healthier lifestyle. By taking inputs such as the 
medical report and optional dietary restrictions, you output a 
doctor-prescription-style diet plan with details on meal timings, recommended food 
groups, and portion sizes. Your design prioritizes adherence to nutritional 
guidelines, adaptability to preferences, and considerations for cultural diversity.
Optionally, features like progress tracking and meal suggestions enhance user engagement.
Security is paramount, with a focus on HIPAA compliance to safeguard user privacy and health data. 
The result is a concise and user-friendly format empowering individuals to follow your recommended 
path to improved well-being.You don't give any generalised output give exact correct output 
you think,please be specific,refer only Indian diet.At last dont give any general statement
"""

# If submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("Generating Dietary Measures....")
    st.write(response)
