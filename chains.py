
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from streamlit.logger import get_logger
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_community.chat_models import BedrockChat

from langchain_community.graphs import Neo4jGraph

from langchain_community.vectorstores import Neo4jVector

from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)

from typing import List, Any
import os
cwd=os.getcwd()
logger = get_logger(__name__)

def load_embedding_model(embedding_model_name: str, logger=logger, config={}):
    if embedding_model_name == "ollama":
        embeddings = OllamaEmbeddings(
            base_url=config["ollama_base_url"], model="llama3"
        )
        dimension = 4096
        logger.info("Embedding: Using Ollama")
    elif embedding_model_name == "openai":
        embeddings = OpenAIEmbeddings()
        dimension = 1536
        logger.info("Embedding: Using OpenAI")
    elif embedding_model_name == "aws":
        embeddings = BedrockEmbeddings()
        dimension = 1536
        logger.info("Embedding: Using AWS")
    elif embedding_model_name == "google-genai-embedding-001":
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001"
        )
        dimension = 768
        logger.info("Embedding: Using Google Generative AI Embeddings")
    else:
        embeddings = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2", cache_folder=f"{cwd}/embedding_model"
        )
        dimension = 384
        logger.info("Embedding: Using SentenceTransformer")
    return embeddings, dimension


def configure_llm_only_chain(llm):
    # LLM only response
    number_of_responses=st.session_state['NUMBER_OF_SUGGESTIONS']
    template = f"""
    אתה בוט שנועד לסייע בקמפיינים עם הצעות לתגובות פוסטים עבור אנשים ליברליים וסובלניים, כותב נגד שחיתות, גזענות, בעד דמוקרטיה ונגד פאשיזם.
שימו לב!!!! אם המשתמש מבקש ממך להשתמש במילים מסוימות, אתה חייב להשתמש בהן בתוך כל תגובה שאתה מספק!!! 
עליך לספק {number_of_responses} תגובות שונות שיכולות לעודד אנשים לפעול או לשתף מחדש.
אתה לא אמור להגיב על שום דבר חוץ מהפוסט
אסור לך לתת עצות מה לעשות
עליך להתמקד בתגובות רלוונטיות לפוסט שנמסר
אתה חייב להשתמש במילים: ״אימפריות נופלות״


    """
    trending_words=st.session_state['TRENDING_WORDS']
    trending_word_template=f"""# :בתשובתך, אתה חייב לכלול את המילים : 
    ״אימפריות נופלות״
    """
    if ("" != trending_words):
        template = template + trending_word_template
    print(template)
    if ("free" in st.session_state['GPT_MODEL_NAME']):
        return(template)
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{question}" 
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    def generate_llm_output(
        user_input: str, callbacks: List[Any], prompt=chat_prompt
    ) -> str:
        chain = prompt | llm
        answer = chain.invoke(
            {"question": user_input}, config={"callbacks": callbacks}
        ).content
        return {"answer": answer}
    
    return generate_llm_output

