#from constants import SCHEMA_IMG_PATH, LANGCHAIN_IMG_PATH
import streamlit as st
import streamlit.components.v1 as components
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

def ChangeButtonColour(wgt_txt, wch_hex_colour = '12px'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('*'), i;
                for (i = 0; i < elements.length; ++i) 
                    { if (elements[i].innerText == |wgt_txt|) 
                        { elements[i].style.color ='""" + wch_hex_colour + """'; } }</script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + wgt_txt + "'")
    components.html(f"{htmlstr}", height=0, width=0)

def AddSampleQuestions(sample_questions):
        st.markdown("""Questions you can ask of the dataset:""", unsafe_allow_html=True)

        # To style buttons closer together
        st.markdown("""
                    <style>
                        div[data-testid="column"] {
                            width: fit-content !important;
                            flex: unset;
                        }
                        div[data-testid="column"] * {
                            width: fit-content !important;
                        }
                   </style>
                    """, unsafe_allow_html=True)
        
        for text, col in zip(sample_questions, st.columns(len(sample_questions))):
            if col.button(text, key=text):
                st.session_state["sample"] = text


class ChainClass:
    def __init__(self):
        self.api_key = st.session_state["USER_OPENAI_API_KEY"] if (("USER_OPENAI_API_KEY" in st.session_state) and (st.session_state["USER_OPENAI_API_KEY"])) else  st.secrets[st.session_state["MODEL_API_KEY_TYPE"]]
        print("api key" + self.api_key, "USER_OPENAI_API_KEY" in  st.session_state ,st.secrets[st.session_state["MODEL_API_KEY_TYPE"]])
        self.api_base=None if "GOOGLE" in st.session_state["MODEL_API_KEY_TYPE"] else st.secrets[st.session_state["MODEL_API_KEY_TYPE"].replace("KEY", "BASE")]
        self.model_name=st.session_state['GPT_MODEL_NAME']
        self.temprature=st.session_state["TEMPERATURE"]
        if "gemini" in self.model_name:
            self.llm = ChatGoogleGenerativeAI(model=self.model_name, google_api_key=self.api_key,temperature=self.temprature, verbose=True,top_k=200)
        else:
            self.llm = ChatOpenAI(model=self.model_name, openai_api_key=self.api_key,openai_api_base=self.api_base,temperature=self.temprature)
    def get_llm_model(self):
        return self.llm
