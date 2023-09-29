import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_sentiment_pipeline():
    return pipeline(model="nlptown/bert-base-multilingual-uncased-sentiment")

@st.cache_resource
def load_skills_regonition_pipeline():
    return pipeline(model="algiraldohe/lm-ner-linkedin-skills-recognition")