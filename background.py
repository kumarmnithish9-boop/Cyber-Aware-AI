import base64
import streamlit as st


def set_background(image_path):

    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(
            image_file.read()
        ).decode()

    st.markdown(
        f"""
        <style>

        .stApp {{

            background-image:
                linear-gradient(
                    rgba(8,18,32,0.92),
                    rgba(8,18,32,0.92)
                ),
                url("data:image/png;base64,{encoded}");

            background-size: cover;

            background-position: center;

            background-repeat: no-repeat;

            background-attachment: fixed;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )