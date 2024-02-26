#!/usr/bin/python3
from models.roadmap import Roadmap
from models.topics import Topic
from models.objectives import Objectives
from models.resources import Resources
import json



# creation of Roadmap
with open('text.json', 'r') as t: 
    data = json.load(t)   
    # with open('data.json', 'w') as f:
    #     json.dump(roadmap, f)

    roadmap_data = {
        'user_id': data['user_id'],
        'title': data['title'],
        'introduction': data['introduction']
    }
    roadmap = Roadmap(**roadmap_data)
    roadmap.save()

    for topic_data in data["topics"]:
        topic = Topic(
            roadmap_id=roadmap.id,
            name=topic_data['name'],
            description=topic_data['description'],
            milestones=topic_data['milestones']
        )

        for objective_text in topic_data['objectives']:
            objective = Objectives(name=objective_text, topic_id=topic.id)
            topic.objectives.append(objective)
            objective.save()

        for resource_link in topic_data['resources']:
            resource = Resources(link=resource_link, topic_id=topic.id)
            topic.resources.append(resource)
            resource.save()

        roadmap.topic.append(topic)
