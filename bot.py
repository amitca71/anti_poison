import os
import openai
import streamlit as st
from streamlit.logger import get_logger
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from common_functions import ChainClass, get_access_token
from google.auth.transport.requests import Request
from chains import (
    configure_llm_only_chain,
    generate_ticket,
)
import requests
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
                vertex_lst=st.secrets["VERTEX_API_BASE"].split(",")
                PROJECT_ID=vertex_lst[0]
                LOCATION=vertex_lst[1]
                ENDPOINT_ID=vertex_lst[2]
                # Prepare the request URL
#                url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}/chat/completions"
                request = Request()
                url = f'https://{LOCATION}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}'
                oai_client = openai.OpenAI(
                    base_url = url,
                    api_key = get_access_token())
####################################################
                number_of_responses=st.session_state['NUMBER_OF_SUGGESTIONS']
                system_prompt=f"תן {number_of_responses} תגובות אפשריות שונות להדהוד הפוסט ברשתות חברתיות, ללא אימוג׳י. מספר את התגובות, הפוסט הוא: "
                user_input=user_input.strip()
                content = f"{user_input} :  {system_prompt}" 
                messages =  [
                    {
                        "role": "user",
                        "content": content.strip(),
#                           "additional_info": "we are in favour of the user"
                    }
                ]
                gen = oai_client.chat.completions.create(
                    model='dicta-il/dictalm2.0-instruct',
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1024,
                    top_p=0.9,
                    stream=False
                )
                full_response = ''
                print (gen)
                result=gen.choices[0].message.content

#                for completion in gen:
#                    text = completion.choices[0].delta.content
#                    if text:
#                        full_response += text.replace('<', '&lt;').replace('>', '&gt;') or ''
#                    yield result

############################################# 
#                number_of_responses=st.session_state['NUMBER_OF_SUGGESTIONS']
#                system_prompt=f"respond with {number_of_responses} responses to post in facebook, the response should courage people to repost it. response should be in hebrew. put serial number on the beggining of each response. dont use emoji within the responses. the original post is"
#                content = f"{user_input} :  {system_prompt}"
 
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

