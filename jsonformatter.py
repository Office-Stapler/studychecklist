import json

with open('data/subjectinfo.json', 'r') as f:
    courses = json.load(f)


for fac in courses:
    for course in courses[fac]:
        course['prereq'] = [x.strip() for x in course['prereq']]


with open('data/subjectinfo.json', 'w') as f:
    json.dump(courses, f, indent=4)