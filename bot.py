import os

import streamlit as st
from streamlit.logger import get_logger
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from common_functions import ChainClass

from chains import (
    configure_llm_only_chain,
    generate_ticket,
)

load_dotenv(".env")
from common_sidebar import common_sidebar
common_sidebar()
ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/")
embedding_model_name = os.getenv("EMBEDDING_MODEL")
#llm_name = os.getenv("LLM", "wizard-vicuna-uncensored")
llm_name = os.getenv("LLM", "mistral")
# Remapping for Langchain Neo4j integration

logger = get_logger(__name__)


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


#llm = load_llm(llm_name, logger=logger, config={"ollama_base_url": ollama_base_url})
llm=ChainClass().get_llm_model()

llm_chain = configure_llm_only_chain(llm)
output_function=None
if type(llm_chain)!=str:
    output_function = llm_chain


# Streamlit UI
styl = f"""
<style>
    /* not great support for :has yet (hello FireFox), but using it for now */
    .element-container:has([aria-label="Select RAG mode"]) {{
      position: fixed;
      bottom: 33px;
      background: white;
      z-index: 101;
    }}
    .stChatFloatingInputContainer {{
        bottom: 20px;
    }}

    /* Generate ticket text area */
    textarea[aria-label="Description"] {{
        height: 200px;
    }}
</style>
"""
st.markdown(styl, unsafe_allow_html=True)


def chat_input():
    user_input=None
    if "sample" in st.session_state and st.session_state["sample"] is not None:
        user_input = st.session_state["sample"]
    else:   
        user_input = st.chat_input("What is the content of the original message?")

    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        with st.chat_message("assistant"):
            stream_handler = StreamHandler(st.empty())
            if (output_function):
                result = output_function(
                    {"question": user_input, "chat_history": []}, callbacks=[stream_handler]
                )["answer"]
            else:
                number_of_responses=st.session_state['NUMBER_OF_SUGGESTIONS']
                max_tokens = 1024
                temperature = st.session_state["TEMPERATURE"]
                top_p = 0.9
                llm_chain="תן תגובות אפשריות שונות להדהוד הפוסט ברשתות חברתיות, ללא אימוג׳י, הפוסט הוא: "
#                llm_chain= "הצע "
                prompt = f"{llm_chain} {user_input} : "
                # Structure your instances for a chat request
                instances = [
                    {
                        "messages": [
                            {"role": "user", "content": prompt.strip()},
                        ],
                        "parameters": {
                            "max_new_tokens": max_tokens,
                            "max_tokens": max_tokens,
                            "temperature": temperature,
                            "top_p": top_p,
#                            "top_k": top_k,
                        },
                    },
                ]

                # Make the prediction call to the chat model
                response = llm.predict(instances)
                result=response.predictions[0]
            output = result
            st.session_state[f"user_input"].append(user_input)
            st.session_state[f"generated"].append(output)


def display_chat():
    # Session state
    if "generated" not in st.session_state:
        st.session_state[f"generated"] = []

    if "user_input" not in st.session_state:
        st.session_state[f"user_input"] = []

    if "rag_mode" not in st.session_state:
        st.session_state[f"rag_mode"] = []

    if st.session_state[f"generated"]:
        size = len(st.session_state[f"generated"])
        # Display only the last three exchanges
        for i in range(max(size - 3, 0), size):
            with st.chat_message("user"):
                st.write(st.session_state[f"user_input"][i])

            with st.chat_message("assistant"):
                st.write(st.session_state[f"generated"][i])

        with st.expander("Not finding what you're looking for?"):
            st.write(
                "Automatically generate a draft for an internal ticket to our support team."
            )
            st.button(
                "Generate ticket",
                type="primary",
                key="show_ticket",
                on_click=open_sidebar,
            )
        with st.container():
            st.write("&nbsp;")


def mode_select() -> str:
    options = ["Disabled", "Enabled"]
    return st.radio("Select RAG mode", options, horizontal=True)






def open_sidebar():
    st.session_state.open_sidebar = True


def close_sidebar():
    st.session_state.open_sidebar = False



chat_input()


display_chat()

