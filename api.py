#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai 
from flask import request


app = Flask(__name__)
CORS(app)

client = openai.Client(
    api_key = "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"
)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
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
