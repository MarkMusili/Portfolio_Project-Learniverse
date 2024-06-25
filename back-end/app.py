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

from flask import Flask, request, jsonify, abort, redirect
from flask_cors import CORS
import openai
import json
from os import environ
from models import storage
from models.auth import Auth

app = Flask(__name__)
CORS(app)
AUTH = Auth()

# Initialize OpenAI client
# client = openai.Client(api_key=environ['OPENAI_API_KEY'])

# Close the database connection at the end of each request
@app.teardown_appcontext
def db_close(exception):
    storage.close()

# @app.route('/')
# def landing_page():
#     """ """
#     return render_template('landing_page.html')

# @app.route('/login')
# def login_page():
#     """ """
#     return render_template('login.html')

# Endpoint for generating chat responses based on prompts
# @app.route('/chat', methods=['POST'])
# def chat():
#     """
#     Generate chat responses based on user prompts using the OpenAI chat model.
#     """
#     data = request.get_json()
#     completion = client.chat.completions.create(
#         model=environ['OPENAI_MODEL_ID'],
#         messages=[
#             {"role": "system", "content": "Given the specific topic, generate a comprehensive learning roadmap in json format. This should include a title for the whole concept, an engaging introduction, a detailed organization of topics and subtopics, learning objectives for each, numerous external links tailored to learners' preferences, time-based milestones, and optional additional information like tips and project ideas. Ensure the roadmap is flexible and diverse to adapt to various learners' needs and goals."},
#             {"role": "user", "content": data["prompt"]}
#         ]
#     )
#     response = completion.choices[0].message.content
#     return jsonify(response)

# Endpoint for rendering the dashboard page
@app.route('/dashboard')
def dashboard():
    """
    Render the dashboard page with a list of available roadmaps.
    """
    roadmap = storage.all("Roadmap").values()
    data = sorted(roadmap, key=lambda k: k.created_at, reverse=True)
    roadmaps = [roadmap.to_dict() for roadmap in data]
    # return render_template('dashboard.html', data=data)
    return jsonify(roadmaps)

# Endpoint for viewing a specific roadmap
@app.route('/roadmap/<roadmap_id>')
def view_roadmap(roadmap_id):
    """
    Render the page for viewing a specific roadmap.
    """
    roadmap = storage.show("Roadmap", roadmap_id)
    if not roadmap:
        return jsonify({'error': 'Roadmap not found'}), 404
    
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

    # return render_template('roadmap.html',
    #                        roadmap=roadmap,
    #                        objectives=objectives,
    #                        topics=sorted(topics.values(), key=lambda t: t.position),
    #                        resources=resources
    #                        )

    return jsonify({
        'roadmap': roadmap.to_dict(),
        'objectives': [obj.to_dict() for obj in objectives],
        'topics': [topic.to_dict() for topic in sorted(topics.values(), key=lambda t: t.position)],
        'resources': [res.to_dict() for res in resources]
    })

# Endpoint for creating a new roadmap
@app.route('/create_roadmap', methods=['POST'])
def create_roadmap():
    """
    Create a new roadmap based on the provided JSON data.
    """
    from models import storage
    from models.roadmap import Roadmap
    from models.topics import Topic
    from models.resources import Resources
    from models.objectives import Objectives

    user_id = request.json.get("user_id")
    roadmap_response = request.json.get("roadmaps")
    if not roadmap_response or not user_id:
        return jsonify({'error': 'Invalid request body'}), 403
    
    user = storage.show("User", user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 400

    
    # for data in roadmap_response:
    roadmap_data = {
        'user_id': user_id,
        'title': roadmap_response['Title'],
        'introduction': roadmap_response['Introduction'],
        'AdditionalInfo': roadmap_response['AdditionalInfo'],
        'planning': True,
        'in_progress': False,
        'completed': False
    }
    roadmap = Roadmap(**roadmap_data)
    roadmap.save()
    r_id = roadmap.id

    position = 1
    for topic_data in roadmap_response["Topics"]:
        topic = Topic(
            position=position,
            roadmap_id=roadmap.id,
            name=topic_data['TopicName'],
            description=topic_data['Descriptions'],
            milestones=topic_data['Milestones']
        )
        position += 1

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
    
    user.roadmaps.append(roadmap)
    user.save()

    return jsonify({'roadmap_id': r_id}), 201

# Endpoint for updating the status of a roadmap
@app.route('/update_roadmap_status/<roadmap_id>', methods=['PUT'])
def update_roadmap_status(roadmap_id):
    """
    Update the status of a roadmap (planning, in_progress, or completed).
    """
    try:
        roadmap = storage.show("Roadmap", roadmap_id)
        if not roadmap:
            return jsonify({'error': 'Roadmap not found'}), 404
        new_status = request.json.get('new_status')
        if not new_status:
            return jsonify({'error': 'Invalid request body'}), 403

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
        return jsonify({'message': f'Roadmap status ({new_status}) updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    
@app.route('/users', methods=["POST"], strict_slashes=False)
def register_user() -> str:
    """
    Register user
    """
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(first_name, last_name, email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    Login method
    """
    email, password = request.form.get("email"), request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """
    Logout method
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect('/')
    # return jsonify({"email": user.email, "message": "Session Destroyed"}), 200

@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    Returns the profile of the session id
    """
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))

    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Get reset password token
    """
    email = request.form.get('email')

    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    Update password
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


# @app.route('/profile')
# def profile_page():
#     """ """
#     return render_template('profile.html')

# @app.route('/settings')
# def settings_page():
#     """ """
#     return render_template('settings.html')

# Test endpoint
@app.route('/', methods=["GET"], strict_slashes=False)
def hello():
    return jsonify({"message": "Hello, this is working"})

if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")
