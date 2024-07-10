from flask import Blueprint, request, jsonify, abort, g
from models import storage
from models.roadmap import Roadmap
from models.topics import Topic
from models.resources import Resources
from models.objectives import Objectives
from auth import login_required

roadmap_bp = Blueprint('roadmap_bp', __name__)

@roadmap_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard page with a list of available roadmaps.
    """
    user = g.user
    roadmap = storage.all("Roadmap", user.id).values()
    data = sorted(roadmap, key=lambda k: k.created_at, reverse=True)
    roadmaps = [roadmap.to_dict() for roadmap in data]

    return jsonify(roadmaps)

@roadmap_bp.route('/create_roadmap', methods=['POST'])
@login_required
def create_roadmap():
    """
    Create a new roadmap based on the provided JSON data.
    """
    from flask import g

    roadmap_response = request.json.get("Roadmap")
    if not roadmap_response:
        abort(400, description="Missing Roadmap")
    
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

@roadmap_bp.route('/roadmap/<roadmap_id>', methods=['GET'])
@login_required
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

    return jsonify({
        'roadmap': roadmap.to_dict(),
        'objectives': [obj.to_dict() for obj in objectives],
        'topics': [topic.to_dict() for topic in sorted(topics.values(), key=lambda t: t.position)],
        'resources': [res.to_dict() for res in resources]
    }), 200

@roadmap_bp.route('/roadmap/<roadmap_id>', methods=['PUT'])
@login_required
def update_roadmap_status(roadmap_id):
    """
    Update the status of a roadmap (planning, in_progress, or completed).
    """
    try:
        roadmap = storage.show("Roadmap", roadmap_id)
        if not roadmap:
            abort(404, description="Roadmap Not Found")

        new_status = request.json.get('new_status')
        if not new_status:
            abort(403, description="Invalid Request body")

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
    
@roadmap_bp.route('/roadmap/<roadmap_id>', methods=["DELETE"], strict_slashes=False)
@login_required
def delete_roadmap(roadmap_id):
    """
    Deletes a Roadmap
    """
    roadmap = storage.show("Roadmap", roadmap_id)
    if not roadmap:
        abort(404, description="Roadmap Not Found")

    storage.delete(roadmap)
    storage.save()
    return jsonify({"message": "Roadmap Deleted Successfully"})
