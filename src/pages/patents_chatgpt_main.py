import streamlit as st
from menu import app_menu
from patents import PatentsHandler

file_name = "/data/streampatents-5000.csv"

handler = PatentsHandler(file_path=file_name)

FILTER_OPTION = {
    "by_inventor": None,
    "is_granted": None,
    "by_publication": None,
    "by_filing": None,
    "by_granted": None
}


def chat_gpt_tab():
    st.title('Ask Chat GPT')


@st.fragment
def form_tab():
    st.title('Query Form')

    with st.container():
        FILTER_OPTION["by_inventor"] = st.selectbox(
            "Select Inventor",
            handler.inventors,
            key="inventors",
            index=None,
            placeholder="Select Inventor...",
        )

        granted = st.radio(
            "Set selectbox label visibility 👉",
            key="granted",
            options=["all", "granted", "no yet granted"],
        )

        if granted == "granted":
            FILTER_OPTION["is_granted"] = True
        elif granted == "no yet granted":
            FILTER_OPTION["is_granted"] = False
        else:
            FILTER_OPTION["is_granted"] = None

        column_1, column_2, column_3 = st.columns(3)

        with column_1:
            FILTER_OPTION["by_filing"] = st.selectbox(
                "Select Filing Year",
                handler.filing_year_range,
                key="by_filing",
                index=None,
                placeholder="Select Filing Year...",
            )

        with column_2:
            FILTER_OPTION["by_publication"] = st.selectbox(
                "Select Publication Year",
                handler.publication_year_range,
                key="by_publication",
                index=None,
                placeholder="Select Publication Year...",
            )

        with column_3:
            FILTER_OPTION["by_granted"] = st.selectbox(
                "Select Granted Year",
                handler.granted_year_range,
                key="by_granted",
                index=None,
                placeholder="Select Granted Year...",
            )

    st.button("Apply Filters")

    st.divider()

    with st.container():

        df = handler.display(**FILTER_OPTION)

        st.dataframe(df)


@st.fragment
def tabs():
    with st.container():
        form, chat_gpt = st.tabs(
            [
                "Query Form",
                "Ask Chat GPT"
            ]
        )

        with form:
            form_tab()

        with chat_gpt:
            chat_gpt_tab()


@st.fragment
def container():
    tabs()


st.set_page_config(
    layout="wide"
)

app_menu()

st.title("Patents Chat GPT Application")
st.header("This application has a Patent DB that you can query either with the widgets or using the chat gpt")

container()
