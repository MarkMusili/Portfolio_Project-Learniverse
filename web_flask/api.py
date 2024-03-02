#!/usr/bin/python3
"""
File: app.py
Description: This file contains the backend implementation of a Flask application for generating and managing learning roadmaps.

Dependencies:
- Flask: Web framework for Python.
- Flask-CORS: Extension for handling Cross-Origin Resource Sharing (CORS).
- OpenAI: Python client for accessing OpenAI's GPT-3 models.
- json: Standard JSON library for Python.
- os.environ: Provides access to environment variables.

Models:
- The application relies on models defined in the 'models' package for database interactions.

Endpoints:
- '/chat': For generating chat responses based on user prompts using OpenAI's chat model.
- '/dashboard': Renders the dashboard page displaying available roadmaps.
- '/roadmap/<roadmap_id>': Renders the page for viewing a specific roadmap.
- '/create_roadmap': Creates a new roadmap based on provided JSON data.
- '/update_roadmap_status/<roadmap_id>': Updates the status of a roadmap (planning, in_progress, or completed).
- '/test': Endpoint for testing if the application is running.

Environment Variables:
- OPENAI_API_KEY: API key for accessing OpenAI services.
- OPENAI_MODEL_ID: ID of the OpenAI model used for generating chat responses.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import json
from os import environ
from models import storage

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = openai.Client(api_key=environ['OPENAI_API_KEY'])

# Close the database connection at the end of each request
@app.teardown_appcontext
def db_close(exception):
    storage.close()

@app.route('/')
def landing_page():
    """ """
    return render_template('landing_page.html')

@app.route('/login')
def login_page():
    """ """
    return render_template('login.html')

# Endpoint for generating chat responses based on prompts
@app.route('/chat', methods=['POST'])
def chat():
    """
    Generate chat responses based on user prompts using the OpenAI chat model.
    """
    data = request.get_json()
    completion = client.chat.completions.create(
        model=environ['OPENAI_MODEL_ID'],
        messages=[
            {"role": "system", "content": "Given the specific topic, generate a comprehensive learning roadmap in json format. This should include a title for the whole concept, an engaging introduction, a detailed organization of topics and subtopics, learning objectives for each, numerous external links tailored to learners' preferences, time-based milestones, and optional additional information like tips and project ideas. Ensure the roadmap is flexible and diverse to adapt to various learners' needs and goals."},
            {"role": "user", "content": data["prompt"]}
        ]
    )
    response = completion.choices[0].message.content
    return jsonify(response)

# Endpoint for rendering the dashboard page
@app.route('/dashboard')
def dashboard():
    """
    Render the dashboard page with a list of available roadmaps.
    """
    roadmap = storage.all("Roadmap").values()
    data = sorted(roadmap, key=lambda k: k.created_at, reverse=True)
    return render_template('dashboard.html', data=data)

# Endpoint for viewing a specific roadmap
@app.route('/roadmap/<roadmap_id>')
def view_roadmap(roadmap_id):
    """
    Render the page for viewing a specific roadmap.
    """
    roadmap = storage.show("Roadmap", roadmap_id)
    topics = storage.fetch("Topic", roadmap.id)
    objectives = []
    resources = []

    for i in topics.values():
        o = storage.fetch("Objectives", i.id)
        r = storage.fetch("Resources", i.id)
        for obj in o.values():
            objectives.append(obj)
        for res in r.values():
            resources.append(res)

    return render_template('roadmap.html',
                           roadmap=roadmap,
                           objectives=objectives,
                           topics=sorted(topics.values(), key=lambda t: t.created_at),
                           resources=resources
                           )

# Endpoint for creating a new roadmap
@app.route('/create_roadmap', methods=['POST'])
def create_roadmap():
    """
    Create a new roadmap based on the provided JSON data.
    """
    from models.roadmap import Roadmap
    from models.topics import Topic
    from models.resources import Resources
    from models.objectives import Objectives

    response = json.loads(request.get_json())
    roadmap_response = response.values()

    for data in roadmap_response:
        roadmap_data = {
            'user_id': "6c970b0d-caed-4ff1-8eee-0ecf04ac7482",
            'title': data['Title'],
            'introduction': data['Introduction'],
            'AdditionalInfo': data['AdditionalInfo'],
            'planning': True,
            'in_progress': False,
            'completed': False
        }
        roadmap = Roadmap(**roadmap_data)
        roadmap.save()
        r_id = roadmap.id

        for topic_data in data["Topics"]:
            topic = Topic(
                roadmap_id=roadmap.id,
                name=topic_data['TopicName'],
                description=topic_data['Descriptions'],
                milestones=topic_data['Milestones']
            )

            for objective_text in topic_data['LearningObjectives']:
                objective = Objectives(name=objective_text, topic_id=topic.id)
                topic.objectives.append(objective)
                objective.save()

            for resource_link in topic_data['Resources']:
                resource = Resources(link=resource_link, topic_id=topic.id)
                topic.resources.append(resource)
                resource.save()

            roadmap.topic.append(topic)
            topic.save()

    return f"{r_id}"

# Endpoint for updating the status of a roadmap
@app.route('/update_roadmap_status/<roadmap_id>', methods=['PUT'])
def update_roadmap_status(roadmap_id):
    """
    Update the status of a roadmap (planning, in_progress, or completed).
    """
    try:
        roadmap = storage.get("Roadmap", roadmap_id)
        new_status = request.json.get('new_status')

        if new_status == 'planning':
            roadmap.planning = True
            roadmap.in_progress = False
            roadmap.completed = False
        elif new_status == 'in_progress':
            roadmap.in_progress = True
            roadmap.planning = False
            roadmap.completed = False
        elif new_status == 'completed':
            roadmap.completed = True
            roadmap.planning = False
            roadmap.in_progress = False

        roadmap.save()
        return jsonify({'message': 'Roadmap status updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# Test endpoint
@app.route('/test')
def hello():
    return "Hello, this is working"

if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")
