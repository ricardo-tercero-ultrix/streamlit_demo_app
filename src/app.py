import streamlit as st
from utils import (
    get_selected_app
)
import os


def main():
    openai_api_key = os.getenv("OPENAI_API_KEY", None)
    if openai_api_key is None or openai_api_key == "NULL":
        st.switch_page("pages/error.py")

    selected_app = get_selected_app()

    if selected_app is None:
        st.switch_page("pages/landing.py")
    else:
        st.switch_page(selected_app["page"])


if __name__ == '__main__':
    main()
