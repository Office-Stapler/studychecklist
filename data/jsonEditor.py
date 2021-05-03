import json

with open('subjectinfo.json', 'r') as f:
    courses = json.load(f)
requirements = dict()
for fac in courses:
    for course in courses[fac]:
        requirements[course['code']] = course['prereq']


with open('prereqs.json', 'w') as f:
    json.dump(requirements, f, indent=4)