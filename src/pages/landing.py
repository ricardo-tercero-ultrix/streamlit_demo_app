import streamlit as st
from utils import (
    open_app,
)

st.title("My Apps")
st.header("This page present my App, please select one of the options")

column_1, column_2, column_3 = st.columns(3)

column_1.title("Text Extractor")
with column_1:
    if st.button("Open App", key="text_extractor"):
        open_app("text_extractor")

column_2.title("Monterrey Gas Price")
with column_2:
    if st.button("Open App", key="mty_gas_price"):
        open_app("mty_gas_price")

column_3.title("Patents Data View")
with column_3:
    if st.button("Open App", key="patents_chatgpt"):
        open_app("patents_chatgpt")
