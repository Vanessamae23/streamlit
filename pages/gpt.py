import streamlit as st
import streamlit.components.v1 as components

try :
    st.set_page_config(page_title="AI Employee Analysis", page_icon = "✈️", layout = "centered", initial_sidebar_state = "auto")
    st.subheader("AI Employee Analysis")

except Exception as e :
    st.error(e)