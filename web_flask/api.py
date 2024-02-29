#!/usr/bin/python3
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import json
from os import environ
from flask import request
from models import storage

app = Flask(__name__)
CORS(app)

client = openai.Client(
    api_key = environ['OPENAI_API_KEY']
)

@app.teardown_appcontext
def db_close(exception):
    storage.close()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    completion = client.chat.completions.create(
        model = environ['OPENAI_MODEL_ID'],
        messages=[
            {"role": "system", "content": "Given the specific topic, generate a comprehensive learning roadmap in json format. This should include a title for the whole concept,an engaging introduction, a detailed organization of topics and subtopics, learning objectives for each, numerous external links tailored to learners' preferences, time-based milestones, and optional additional information like tips and project ideas. Ensure the roadmap is flexible and diverse to adapt to various learners' needs and goals."},
            {"role": "user", "content": data["prompt"]}
        ]
    )
    response = completion.choices[0].message.content
    return jsonify(response)

@app.route('/dashboard')
def dashboard():
    roadmap = storage.all("Roadmap").values()
    data = sorted(roadmap, key=lambda k: k.created_at, reverse=True)
    return render_template('dashboard.html', data=data)

@app.route('/roadmap/<roadmap_id>')
def view_roadmap(roadmap_id):
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
            topics=sorted(topics, lambda t: t.created_at),
            resources=resources
            )

@app.route('/create_roadmap', methods=['POST'])
def create_roadmap():
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

@app.route('/update_roadmap_status/<roadmap_id>', methods=['PUT'])
def update_roadmap_status(roadmap_id):
    try:
        roadmap = storage.get("Roadmap", roadmap_id)
        new_status = request.json.get('new_status')

        # Update the boolean variables based on the new status
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

@app.route('/test')
def hello():
   return "Hello this is working"

if __name__ == "__main__":
  app.run(debug=True, port=8080, host="0.0.0.0")
