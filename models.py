import json
import streamlit as st
from transformers import pipeline
import openai

@st.cache_resource
def load_sentiment_pipeline():
    return pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")

@st.cache_resource
def load_skills_recognition_pipeline():
    return pipeline("token-classification", model="algiraldohe/lm-ner-linkedin-skills-recognition")


ROLE_PLAY_HUMAN_RESOURES_PROMPT = "As a professional human resources manager, give recommendations for upskilling and career development in an encouraging and motivating tone to the following employee with profile."

openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_recommendations(employee_data):
    content = ROLE_PLAY_HUMAN_RESOURES_PROMPT + parse_employee_data(employee_data)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user", "content": content}],
        temperature=0.6
    )
    return {
        "Recommendations": response.choices[0].message.content
    }

def parse_employee_data(employee_data):
    data_json = json.dumps(employee_data.val(), indent=4)
    data_dict = json.loads(data_json)
    if 'skillsReview' not in data_dict:
        return ""
    return "Name:{}, Position:{}, Skills Review:{}, Education:{}".format(data_dict['name'], data_dict['position'], data_dict['skillsReview'], data_dict['education'])