import streamlit as st
from pyudemy import Udemy
import streamlit.components.v1 as components
from models import load_skills_recognition_pipeline

try :
    st.set_page_config(page_title="AI Employee Analysis", page_icon = "✈️", layout = "centered", initial_sidebar_state = "auto")
    st.subheader("AI Employee Analysis")
    udemy = Udemy(st.secrets['UDEMY_CLIENT_ID'], st.secrets['UDEMY_CLIENT_SECRET'])
    example = [
        {
            "Object" : "course",
            "Setting": "@min"
        }
    ]
    data =(udemy.courses(page=1, page_size=10, search='java'))

    for i, val in enumerate(data['results']) :
        uri = "https://www.udemy.com/" + val['url']
        st.write("Check out this ", uri)
        st.image(val['image_240x135'])
        st.text(val['title'])
    
except Exception as e :
    st.error(e)