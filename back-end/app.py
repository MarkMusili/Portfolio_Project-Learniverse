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
- '/users' [POST]: Creates a new user
- '/sessions' [POST]: 
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

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from controllers.chat_controller import chat_bp
from controllers.roadmap_controller import roadmap_bp
from controllers.user_controller import user_bp
from models import storage
from os import getenv
import openai

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
load_dotenv()
openai.api_key = getenv('OPENAI_API_KEY')

# Register Blueprints
app.register_blueprint(chat_bp)
app.register_blueprint(roadmap_bp)
app.register_blueprint(user_bp)

# Close the database connection at the end of each request
@app.teardown_appcontext
def db_close(exception):
    storage.close()

# Test endpoint
@app.route('/', methods=["GET"], strict_slashes=False)
def hello():
    return jsonify({"message": "Welcome to Learniverse"})

# Custom Error Handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"Error": str(error.description)}), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"Error": str(error.description)}), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({"Error": str(error.description)}), 403

@app.errorhandler(404)
def not_found(error):
    return jsonify({"Error": str(error.description)}), 404

if __name__ == "__main__":
    app.run(debug=True)
