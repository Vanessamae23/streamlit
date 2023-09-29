import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_sentiment_pipeline():
    return pipeline(model="nlptown/bert-base-multilingual-uncased-sentiment")
