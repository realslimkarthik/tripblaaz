import json
from travel_tracker.models import db, User, Group, Landmark, User_Group


def generate_landmark_json(group_id):
    group = Group.query.filter(id=group_id)
    landmarks = Landmark.query.filter(group_id=group_id).all()
    group_json_object = {}
    group_json_object['group_id'] = group_id
    group_json_object['name'] = group.name
    group_json_object['description'] = group.description
    group_json_object['landmarks'] = []
    for landmark in landmarks:
        landmark_json = {}
        landmark_json['landmark_id'] = landmark.id
        landmark_json['name'] = landmark.name
        landmark_json['lat'] = landmark.lat
        landmark_json['lng'] = landmark.lng
        group_json_object['landmarks'].append(landmark_json)

    return json.dumps(group_json_object)
