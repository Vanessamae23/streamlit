import json
import streamlit as st
from transformers import pipeline
import openai

@st.cache_resource
def load_sentiment_pipeline():
    return pipeline(model="nlptown/bert-base-multilingual-uncased-sentiment")

@st.cache_resource
def load_skills_regonition_pipeline():
    return pipeline(model="algiraldohe/lm-ner-linkedin-skills-recognition")


ROLE_PLAY_HUMAN_RESOURES_PROMPT = "As a professional human resources manager, give recommendations for upskilling and career development in an encouraging and motivating tone to the following employee with profile:"

openai.api_key = st.secrets["API_KEY"]

def generate_recommendations(employee_data):
    # content = ROLE_PLAY_HUMAN_RESOURES_PROMPT + parse_employee_data(employee_data)
    # response = openai.Completion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role":"user", "content": content}],
    #     temperature=0.6
    # )
    # return {
    #     "ai_recommendations": response.choices[0].message.content
    # }
    return parse_employee_data(employee_data)

def parse_employee_data(employee_data):
    data_json = json.dumps(employee_data.val(), indent=4)
    data_dict = json.loads(data_json)
    return "Name:{}\n Position:{}\n Skills Review:{}\n Education:{}".format(data_dict['name'], data_dict['position'], data_dict['skillsReview'], data_dict['education'])