#!/usr/bin/python3
from models.roadmap import Roadmap
from models.topics import Topic
from models.objectives import Objectives
from models.resources import Resources
import json

# creation of Roadmap
with open('text.json', 'r') as t: 
    roadmap = json.load(t).values()
    # with open('data.json', 'w') as f:
    #     json.dump(roadmap, f)

    for data in roadmap:
        roadmap_data = {
            'user_id': "0d54ee7c-7414-46f0-861c-b51486114282",
            'title': data['Title'],
            'introduction': data['Introduction']
        }
        roadmap = Roadmap(**roadmap_data)
        roadmap.save()

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

