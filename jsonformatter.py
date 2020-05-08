import json

with open('data/subjectinfo.json', 'r') as f:
    courses = json.load(f)

with open('data/subjectinfo.json', 'w') as f:
    json.dump(courses, f, indent=4)