import streamlit as st
from utils import (
    get_selected_app
)


def main():

    selected_app = get_selected_app()

    if selected_app is None:
        st.switch_page("pages/landing.py")
    else:
        st.switch_page(selected_app["page"])




if __name__ == '__main__':
    main()
