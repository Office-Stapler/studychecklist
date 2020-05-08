import requests
from bs4 import BeautifulSoup
import re
import json

with open('data/subjectinfo.json', 'r') as f:
    courses = json.load(f)

for fac in courses:
    for i in courses[fac]:
        url = f"https://www.handbook.unsw.edu.au/undergraduate/courses/2020/{i['code']}"
        print(i['code'])
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        data = soup.find_all(id='SubjectConditions')
        string = BeautifulSoup(str(data), 'html.parser')
        if data != []:
            search = re.search('Prerequisite:(.*)</div>' , str(string))
            if search != None:
                string = search.group(1)
                i['prereq'] = string
                with open('data/subjectinfo.json', 'w') as f:
                    json.dump(courses, f)
                print(string)

