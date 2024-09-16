import pytesseract
import streamlit as st
from PIL import Image
from menu import app_menu

SELECTED_IMAGE = None

def extract_text_from_image(img) -> str:
    text = pytesseract.image_to_string(img, lang='spa')
    return text

@st.fragment()
def container():
    global SELECTED_IMAGE

    if SELECTED_IMAGE is not None:
        with st.container():
            st.text("Selected Image")
            st.image(SELECTED_IMAGE)

        with st.container():
            extracted_text = None
            with st.spinner('Wait for it...'):
                extracted_text = extract_text_from_image(SELECTED_IMAGE)
            if extracted_text is not None and len(extracted_text) > 0:
                st.success(extracted_text)
            else:
                st.error("Text not found")

    else:
        with st.container():
            st.text("Select Image or Take a Picture")

        with st.container():
            col_1, col_2 = st.columns(2)
            with col_1:
                uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg'])

            with col_2:
                uploaded_file = st.camera_input("Take a picture")

            if uploaded_file is not None:
                SELECTED_IMAGE = Image.open(uploaded_file)
                st.button("Process Image")
app_menu()

st.title("Text Extractor Application")
st.header("This app receive an image/photo and extract the Text on it")

container()