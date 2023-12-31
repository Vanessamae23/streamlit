import json
import math
import streamlit as st
import pandas as pd
from pyudemy import Udemy
import streamlit.components.v1 as components
from firebase import db
from models import load_skills_recognition_pipeline
from streamlit_card import card

try :
    st.set_page_config(layout="wide", page_title="AI Employee Analysis", page_icon = "✈️",  initial_sidebar_state = "auto")
    st.subheader("AI Employee Analysis")


    data = db.child('employees').get()
    json_data = json.dumps(data.val(), indent=4)
    json_dict = json.loads(json_data)
    df = pd.DataFrame(json_dict.values())[['id', 'name', 'email', 'skillsReview']]

    pipeline = load_skills_recognition_pipeline()

    df['Skills Interested'] = df['skillsReview'].apply(lambda x: ','.join(map(lambda x: x['word'], pipeline.group_entities(pipeline(x if pd.notnull(x) else "")))))


    th_props = [
    ('font-size', '14px'),
    ('text-align', 'left'),
    ('font-weight', 'bold'),
    ('color', '#fff'),
    ('text-transform', 'uppercase'),
    ('background-color', '#808080')
    ]
                                    
    td_props = [
        ('font-size', '12px'),
        ('text-align', 'left'),
        ]
    styles = [
        dict(selector="th", props=th_props),
        dict(selector="td", props=td_props)
    ]

    df.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles)
    st.table(df)

    selected_employees = st.multiselect(
        "Select Employee",
        df['name'])

    udemy = Udemy(st.secrets['UDEMY_CLIENT_ID'], st.secrets['UDEMY_CLIENT_SECRET'])
    example = [
        {
            "Object" : "course",
            "Setting": "@min"
        }
    ]
    
    employee_ids = df.loc[df['name'].isin(selected_employees)]['id'].tolist()
    udemy_search_keywords = df.loc[df['name'].isin(selected_employees)]['Skills Interested'].apply(lambda x: x.split(',')).explode().unique().tolist()

    data = (udemy.courses(page=1, page_size=10, search=udemy_search_keywords))


    for val in data['results'][:10]:
        card(
            title = val['title'],
            text = val['headline'],
            image = val['image_240x135'],
            url = "https://www.udemy.com" + val['url'],
            styles={
            "card": {
                "padding": "0",
                "width": "300px",
                "height": "300px"
                }
            }
        )
    
    # for employee_id in employee_ids:
    #     db.child("recommended_courses").child(employee_id).set(list(map(lambda x: x.title, data['results'][:10])))
except Exception as e :
    st.error(e)