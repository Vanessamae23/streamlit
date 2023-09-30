import streamlit as st
import json
from pyudemy import Udemy
import streamlit.components.v1 as components

try :
    st.set_page_config(page_title="AI Employee Analysis", page_icon = "✈️", layout = "centered", initial_sidebar_state = "auto")
    st.subheader("AI Employee Analysis")
    udemy = Udemy("lMJ7wdS2looOAxZ4aoirfTVnIYWJFgttkYMznkzU", "DxuFUhcXHOGp5C5xoEb93LTiXiRETFtQ7aCxNq62wFCLP8aEjpwIYiueVhGgxSRJFfm9kXD1PasDbeSTz5pddSLWD4r3oKJGDc6eSrfCQgHG9S9m7SQny3XtTxpHgM6K")
    example = [
        {
            "Object" : "course",
            "Setting": "@min"
        }
    ]
    data =(udemy.courses(subcategory= 'Communication',page=1, page_size=10))

    for i, val in enumerate(data['results']) :
        uri = "https://www.udemy.com/" + val['url']
        st.write("Check out this ", uri)
        st.image(val['image_240x135'])
        st.text(val['title'])
    
except Exception as e :
    st.error(e)