from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image  
import google.generativeai as genai

load_dotenv()
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(input,image):
    if input !="":
        response=model.generate_content([input,image])
        parts=response.candidates[0].content.parts
        text=' '.join(part.text for part in parts)
        return text
    
## Initialize streamlit app
st.set_page_config(page_title="Gemini Image Demo")
st.header("Invoice Extractor")
input=st.text_input("Input Promt:", key="input")
uploaded_file=st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image.")

submit=st.button("Tell me about the image")

## If ask button is clicked
if submit:
    response=get_gemini_response(input,image)
    st.subheader("The Response is")
    st.write(response)