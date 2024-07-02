from flask import Blueprint, request, jsonify
import openai
from os import getenv
from auth import login_required

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    """
    Generate chat responses based on user prompts using the OpenAI chat model.
    """
    data = request.get_json()
    completion = openai.ChatCompletion.create(
        model=getenv('OPENAI_MODEL_ID'),
        messages=[
            {"role": "system", "content": "Given the specific topic, generate a comprehensive learning roadmap in json format. This should include a title for the whole concept, an engaging introduction, a detailed organization of topics and subtopics, learning objectives for each, numerous external links tailored to learners' preferences, time-based milestones, and optional additional information like tips and project ideas. Ensure the roadmap is flexible and diverse to adapt to various learners' needs and goals."},
            {"role": "user", "content": data["prompt"]}
        ]
    )
    response = completion.choices[0].message['content']
    return jsonify(response)