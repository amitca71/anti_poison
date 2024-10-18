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
#            st.session_state["K_TOP"]= st.radio(
#                "K top:",
#                ("3","5","10","15"), index=2,horizontal=True
#            )
            st.session_state["NUMBER_OF_SUGGESTIONS"] = st.slider('Number of suggestions', 1, 20, 7, step=1)
            st.session_state["TEMPERATURE"] = st.slider('Temperature - higher=more creative', 0.0, 1.0, 0.0, step=0.0001)

        # Optionally visualize graph data using third-party libraries

        sample_questions = ["ידע כל בורג במכונת הרעל - הזמנים בהם אתם משחקים מול מגרש ריק - הסתיימו.", \
            "בואו. זה חשוב, מסר מפרופ׳ שקמה ברסלר לקראת הצעדה מחר ", \
                "זה לא ציר פילדלפי, זה ספין פילדלפי",\
            "רביב דרוקר בכנס חירום בצוותא להצלת חדשות 13 גם אמנון אברמוביץ ויונית לוי הגיעו לתמוך שאפו ענק" ,
            """ סגורים! ✈️ ✈️

היא לא נקפה אצבע בשביל תחבורה ציבורית למילואימניקים 🪖

את רוב הזמן שלה היא מכלה בארגון טקסים 🎊

ובזמן מלחמה היא גם אחראית לקריסה מוחלטת מול חברות התעופה הזרות, שמחזירה אותנו עשרות שנים אחורה 🌍

בזמן שישראל מותקפת ע״י אירן, מירי רגב נסעה לביקור אצל החבר אורבן בהונגריה 🇭🇺🚀

״זאת הנסיעה שתפתור את משבר הטיסות״ הסבירו לנו במשרד המגוחך שלה….

אז הנה! היום בצהריים הודיעה ענקית הלואו קוסט ההונגרית, Wizz על הפסקת הטיסות לישראל עד 2025!

מלכת השמיים הסגורים """]

        AddSampleQuestions(sample_questions)



  