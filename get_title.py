#!/usr/bin/python3
""" Fetch the title of a roamdap """
import sys
from models import storage

roadmap = storage.show("Roadmap", "451e0720-31c9-4dce-a5ec-443f07259cf2")
print(roadmap)
print()

topics = storage.all("Topic").values()
topics = list(filter(lambda topic: topic.roadmap_id == roadmap.id, topics))

topics = [topic.to_dict() for topic in topics]

for topic in topics:
    print(topic['name'])
    print(topic['description'])
    print(topic['milestones'])

    objectives = storage.all('Objectives').values()
    objectives = list(filter(lambda objective: objective.topic_id == topic['id'], objectives))
    objectives = [o.to_dict() for o in objectives]
    for objective in objectives:
        print(f"--------------{objective['name']}")
    print()
