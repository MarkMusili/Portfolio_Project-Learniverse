#!/usr/bin/python3
"""

"""
from flask import Blueprint, jsonify, abort, g
from models import storage
from auth.decorators import login_required
from utils.request_utils import get_request_data


roadmap_bp = Blueprint('roadmap_bp', __name__)

@roadmap_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard page with a list of available roadmaps.
    """
    user = g.user
    print(user.id)
    roadmaps = storage.all("Roadmap", f'{user.id}').values()
    sorted_roadmaps = sorted(roadmaps, key=lambda k: k.created_at, reverse=True)

    return jsonify([roadmap.to_dict() for roadmap in sorted_roadmaps])

@roadmap_bp.route('/create_roadmap', methods=['POST'])
@login_required
def create_roadmap():
    """
    Create a new roadmap based on the provided JSON data.
    """
    from models.roadmap import Roadmap
    from models.topics import Topic
    from models.resources import Resources
    from models.objectives import Objectives

    roadmap_response = get_request_data(["Roadmap"])["Roadmap"]

    user_id = g.user.id
    user = storage.show("User", user_id)
    if not user:
        abort(404, description=f"User id: {user_id} Not Found")

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

    for position, topic_data in enumerate(roadmap_response["Topics"], start=1):
        topic = Topic(
            position=position,
            roadmap_id=roadmap.id,
            name=topic_data['TopicName'],
            description=topic_data['Descriptions'],
            milestones=topic_data['Milestones']
        )
        topic.save()

        for objective_text in topic_data['LearningObjectives']:
            objective = Objectives(name=objective_text, topic_id=topic.id)
            objective.save()

        for resource_link in topic_data['Resources']:
            resource = Resources(link=resource_link, topic_id=topic.id)
            resource.save()

    return jsonify({'roadmap_id': roadmap.id}), 201

@roadmap_bp.route('/roadmap/<roadmap_id>', methods=['GET'])
@login_required
def view_roadmap(roadmap_id):
    """
    Render the page for viewing a specific roadmap.
    """
    roadmap = storage.show("Roadmap", roadmap_id)
    if not roadmap:
        return jsonify({'error': 'Roadmap not found'}), 404

    topics = storage.fetch("Topic", roadmap.id).values()
    objectives = [obj for topic in topics for obj in storage.fetch("Objectives", topic.id).values()]
    resources = [res for topic in topics for res in storage.fetch("Resources", topic.id).values()]

    return jsonify({
        'roadmap': roadmap.to_dict(),
        'objectives': [obj.to_dict() for obj in objectives],
        'topics': [topic.to_dict() for topic in sorted(topics, key=lambda t: t.position)],
        'resources': [res.to_dict() for res in resources]
    }), 200

@roadmap_bp.route('/roadmap/<roadmap_id>', methods=['PUT'])
@login_required
def update_roadmap_status(roadmap_id):
    """
    Update the status of a roadmap (planning, in_progress, or completed).
    """
    roadmap = storage.show("Roadmap", roadmap_id)
    if not roadmap:
        abort(404, description="Roadmap Not Found")

    new_status = get_request_data(['new_status'])['new_status']
    valid_statuses = ['planning', 'in_progress', 'completed']
    if new_status not in valid_statuses:
        abort(400, description="Invalid status")

    roadmap.planning = new_status == 'planning'
    roadmap.in_progress = new_status == 'in_progress'
    roadmap.completed = new_status == 'completed'
    roadmap.save()

    return jsonify({'message': f'Roadmap status ({new_status}) updated successfully'}), 200

@roadmap_bp.route('/roadmap/<roadmap_id>', methods=["DELETE"], strict_slashes=False)
@login_required
def delete_roadmap(roadmap_id):
    """
    Delete a Roadmap.
    """
    roadmap = storage.show("Roadmap", roadmap_id)
    if not roadmap:
        abort(404, description="Roadmap Not Found")

    storage.delete(roadmap)
    storage.save()
    return jsonify({"message": "Roadmap Deleted Successfully"}), 200
