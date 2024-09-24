#from constants import SCHEMA_IMG_PATH, LANGCHAIN_IMG_PATH
import streamlit as st
import streamlit.components.v1 as components
import json
from promote_post_sidebar import promote_post_sidebar
#from technical_objects_sidebar import technical_objects_sidebar


# Streamlit app layout
#st.title("Building Information Modeling")

# Get all secrets
models_dct = {v: k.split("_")[3] + "_API_KEY" for  k,v in st.secrets.items() if "GPT_MODEL_NAME" in k }
print (models_dct)

def ChangeButtonColour(wgt_txt, wch_hex_colour = '12px'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('*'), i;
                for (i = 0; i < elements.length; ++i) 
                    { if (elements[i].innerText == |wgt_txt|) 
                        { elements[i].style.color ='""" + wch_hex_colour + """'; } }</script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + wgt_txt + "'")
    components.html(f"{htmlstr}", height=0, width=0)

def common_sidebar():
    with st.sidebar:
        page=st.sidebar.selectbox("Select a page", ["repost positive", "Response to racism" ])

        # Display different content based on the selected page
        model_name = st.selectbox(
            "select model- beaware: no free quote for gpt-4o!!",
            models_dct.keys(),
        )
        st.write("selected model:", model_name)
        with st.expander(f"""Model Key- (needed after free quota is exahusted)"""):
            new_oak = st.text_input("Your API Key")
            # if "USER_OPENAI_API_KEY" not in st.session_state:
            #     st.session_state["USER_OPENAI_API_KEY"] = new_oak
            # else:
            st.session_state["USER_OPENAI_API_KEY"] = new_oak

        st.session_state["MODEL_API_KEY_TYPE"]=models_dct[model_name]
        st.session_state["GPT_MODEL_NAME"]=model_name
        if page == "repost positive":
            print("repost positive")
            st.session_state["USER_SELECTION"]="REPOST_POSITIVE"
            promote_post_sidebar()
#        elif page == "Technical documentation":
#            st.session_state["USER_SELECTION"]="DOCUMENTATION"
#            technical_doc_sidebar()
#        elif page == "Bim Objects":
#            st.session_state["USER_SELECTION"]="BIM_OBJECTS"
#            technical_objects_sidebar()


 