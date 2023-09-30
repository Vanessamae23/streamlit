import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


ROLE_PLAY_HUMAN_RESOURES_PROMPT = "As a professional human resources manager, give recommendations for upskilling and career development to the following employee in an encouraging and motivating tone."


@app.route("/", methods=("POST"))
def index():
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user", "content": ROLE_PLAY_HUMAN_RESOURES_PROMPT}]
        temperature=0.6,
    )
    return {
        "ai_recommendations": response.choices[0].message.content
    }
