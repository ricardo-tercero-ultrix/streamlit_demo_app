import streamlit as st
from utils import (
    close_app,
    go_app_landing,
    get_selected_app,
)


def menu() -> None:
    st.sidebar.header("Menu")
    st.sidebar.markdown("---")
    st.sidebar.page_link("pages/landing.py", label="Home")
    st.sidebar.page_link("pages/close_app.py", label="Close App")

def app_menu() -> None:
    selected_app = get_selected_app()
    if selected_app is None:
        st.switch_page("app.py")
    with st.container():
        if st.button("Home"):
            go_app_landing()
        if st.button("Close App"):
            close_app()