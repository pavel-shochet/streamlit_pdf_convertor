import os
from pdf2docx import Converter
import streamlit as st

# Streamlit UI
st.title("PDF to Word Converter")
st.write("Upload a PDF file to convert it into a Word document.")

# File upload
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    # File name input
    default_name = os.path.splitext(uploaded_file.name)[0] + "_converted"  # Default custom name
    custom_name = st.text_input(
        "Enter a name for the output file (without extension):", default_name
    )

    if st.button("Convert"):
        # Save uploaded file temporarily
        pdf_path = f"temp_{uploaded_file.name}"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())

        # Add .docx extension to the custom name
        word_file_name = f"{custom_name}.docx"
        word_path = f"temp_{word_file_name}"

        # Convert PDF to Word
        st.write("Converting your file...")
        cv = Converter(pdf_path)
        cv.convert(word_path, start=0, end=None)  # Convert all pages
        cv.close()

        # Read the converted file for download
        with open(word_path, "rb") as f:
            file_data = f.read()

        # Display Streamlit's download button
        st.download_button(
            label="Download Converted Word File",
            data=file_data,
            file_name=word_file_name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

        # Clean up temporary files
        os.remove(pdf_path)
        os.remove(word_path)
