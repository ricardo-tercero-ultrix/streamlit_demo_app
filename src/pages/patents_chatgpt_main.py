import streamlit as st
from menu import app_menu
from patents import PatentsHandler
from constants import (
    PATENT_CHAT_BOT_NAME,
    PATENT_FILE_NAME,
)
from patents_utils import summarize_patent
from langchain_utils import ask_question

@st.cache_data
def get_handler():
    return PatentsHandler(file_path=PATENT_FILE_NAME)

FILTER_OPTION = {
    "by_inventor": None,
    "is_granted": None,
    "by_publication": None,
    "by_filing": None,
    "by_granted": None
}


@st.cache_data
def ask_question_to_chatbot(question):
    handler = get_handler()
    return ask_question(
        df=handler.df,
        question=question,
    )


@st.fragment
def chat_gpt_tab():
    st.title('Ask Chat GPT')

    for entry in st.session_state[PATENT_CHAT_BOT_NAME]:
        st.chat_message(name=entry["role"]).write(entry["content"])

    with st.container():
        user_prompt = st.chat_input("Ask Something about patents.")
        st.write(user_prompt)
        if user_prompt:
            st.session_state[PATENT_CHAT_BOT_NAME].append({"role": "human", "content": user_prompt})

            with st.spinner("Waiting for the answer..."):
                try:
                    response = ask_question_to_chatbot(user_prompt)
                    st.session_state[PATENT_CHAT_BOT_NAME].append({"role": "assistant", "content": response})
                except Exception as e:
                    st.warning(str(e))


@st.cache_data
@st.dialog("Patent Summary")
def view_patent_summary(patent_id: str):
    handler = get_handler()
    summary = summarize_patent(patent_id=patent_id, handler=handler)
    st.write(summary)

@st.fragment
def form_tab():
    st.title('Query Form')
    handler = get_handler()
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

        event = st.dataframe(
            df,
            key="data",
            on_select="rerun",
            selection_mode=["single-row"],
        )
        selected_row = event.selection.get("rows", [])
        if len(selected_row) > 0:
            if st.button("View Patent Summary"):
                selected_index = selected_row[0]
                selected_data_row = df.iloc[selected_index]
                patent_id = selected_data_row["id"]
                view_patent_summary(patent_id=patent_id)


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

if PATENT_CHAT_BOT_NAME not in st.session_state:
    st.session_state[PATENT_CHAT_BOT_NAME] = [{"role": "assistant", "content": "What can I do for you?"}]

app_menu()

st.title("Patents Chat GPT Application")
st.header("This application has a Patent DB that you can query either with the widgets or using the chat gpt")

container()
