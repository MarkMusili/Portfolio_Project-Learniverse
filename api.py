#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from os import environ
from flask import request


app = Flask(__name__)
CORS(app)

client = openai.Client(
    api_key = os.environ['OPENAI_API_KEY']
)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    completion = client.chat.completions.create(
        model=os.environ['OPENAI_MODEL_ID'],
        messages=[
            {"role": "system", "content": "You are an"},
            {"role": "user", "content": data["prompt"]}
        ]
    )
    response = completion.choices[0].message.content
    return jsonify(response)

@app.route('/test')
def hello():
   return "Hello this is working"

if __name__ == "__main__":
  app.run(debug=True, )
