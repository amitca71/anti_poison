import os
import openai
import streamlit as st
from streamlit.logger import get_logger
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from common_functions import ChainClass, get_access_token, get_model_endpoint
from google.auth.transport.requests import Request
from chains import (
    configure_llm_only_chain
)
import requests
load_dotenv(".env")
from common_sidebar import common_sidebar
common_sidebar()
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


llm=ChainClass().get_llm_model()

llm_chain = configure_llm_only_chain(llm)
output_function=None
#if type(llm_chain)!=str:
#    output_function = llm_chain



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
        user_input = st.chat_input("write the content of the original message?")

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
                print("No output function")
                PROJECT_ID=st.secrets["PROJECT_ID"]
                LOCATION=st.secrets["LOCATION"]
 
                models_deployed, url=get_model_endpoint(project_id=PROJECT_ID, location=LOCATION)
                if (not models_deployed):
                    print("not deployed yet")

                oai_client = openai.OpenAI(
                    base_url = url,
                    api_key = get_access_token())

####################################################
                number_of_responses=st.session_state['NUMBER_OF_SUGGESTIONS']
                trending_words=st.session_state["TRENDING_WORDS"]
#                system_prompt=f"תן {number_of_responses} תגובות אפשריות שונות להדהוד הפוסט ברשתות חברתיות, ללא אימוג׳י. המשתמש יכול לתת לך הכוונה במה להתמקד בתשובה, בסוף הטקסט, אחרי המילים: ״הוראות מיוחדות״. אם הוא עושה זאת, כל התגובות חייבות להיות ברוח זו !!!!!!!!. התגובות ללא האשטאגים. מספר את התגובות, הפוסט הוא: "
                system_prompt=st.session_state["SYSTEM_PROMPT"]
                user_input = user_input + f""".\nֿ\n ֿֿֿהוראות מיוחדות עבור כל התגובות המוצעות: {trending_words} !!!.\n\n"""
                user_input=user_input.strip()
                content = f"{user_input} :  {system_prompt}" 
                messages =  [
                    {
                        "role": "user",
                        "content": content.strip(),
                        "additional_info":  f"{trending_words}"
                    }
                ]
                gen = oai_client.chat.completions.create(
                    model='dicta-il/dictalm2.0-instruct',
                    messages=messages,
                    temperature=0,
                    max_tokens=4000,
                    top_p=0.9,
                    stream=False
                )
                full_response = ''
                print (gen)
                result=gen.choices[0].message.content

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

