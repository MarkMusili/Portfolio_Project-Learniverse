#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from os import environ
from flask import request


app = Flask(__name__)
CORS(app)

client = openai.Client(
    api_key = environ['OPENAI_API_KEY']
)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    completion = client.chat.completions.create(
        model = environ['OPENAI_MODEL_ID'],
        messages=[
            {"role": "system", "content": "Given the specific topic, generate a comprehensive learning roadmap in json format. This should include a title for the whole concept,an engaging introduction, a detailed organization of more than 2 topics and subtopics, learning objectives for each, numerous external links tailored to learners' preferences, time-based milestones, and optional additional information like tips and project ideas. Ensure the roadmap is flexible and diverse to adapt to various learners' needs and goals."},
            {"role": "user", "content": data["prompt"]}
        ]
    )
    response = completion.choices[0].message.content
    return jsonify(response)

@app.route('/test')
def hello():
   return "Hello this is working"

if __name__ == "__main__":
  app.run(debug=True, port=8080, host="0.0.0.0")