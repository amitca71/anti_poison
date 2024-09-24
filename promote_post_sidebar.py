#from constants import SCHEMA_IMG_PATH, LANGCHAIN_IMG_PATH
import streamlit as st
import streamlit.components.v1 as components
import json
from common_functions import AddSampleQuestions


def promote_post_sidebar():
    with st.sidebar: 
    # Streamlit app layout
        st.title("Promote post")
        with st.sidebar:
            st.session_state["K_TOP"]= st.radio(
                "K top:",
                ("3","5","10","15"), index=2,horizontal=True
            )

        # Optionally visualize graph data using third-party libraries

        sample_questions = ["ידע כל בורג במכונת הרעל - הזמנים בהם אתם משחקים מול מגרש ריק - הסתיימו.", \
            "בואו. זה חשוב, מסר מפרופ׳ שקמה ברסלר לקראת הצעדה מחר ", \
                "זה לא ציר פילדלפי, זה ספין פילדלפי",\
            "רביב דרוקר בכנס חירום בצוותא להצלת חדשות 13 גם אמנון אברמוביץ ויונית לוי הגיעו לתמוך שאפו ענק" ]

        AddSampleQuestions(sample_questions)



  