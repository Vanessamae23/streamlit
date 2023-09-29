import streamlit as st
import pandas as pd

@st.cache_resource
def load_related_skills_df():
    return pd.read_csv("data/related_skills.csv")
