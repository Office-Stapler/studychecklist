import bs4
import requests
import json
import re

def get_info_subject(subject):
    url = f'http://timetable.unsw.edu.au/2020/{subject}KENS.html'
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    subjects = soup.find_all('td', class_='data')[9:]
    names = [x.get_text() for x in subjects[:-1:3]]
    units = []
    for i in subjects[1:-1:3]:
        try:
            unit = int(i.get_text())
        except:
            continue
        units.append(unit)

    codes = [x.get_text() for x in subjects[2:-1:3]]
    final = list(zip(codes, names, units))
    with open('subjectinfo.json', 'r+') as f:
        courses = json.load(f)
        f.seek(0)
        courses.extend(final)
        json.dump(courses, f, indent=4)
    
    

with open('subjectarea.json', 'r') as f:
    subjects = json.load(f)

for subject in subjects:
    get_info_subject(subject[1])
    print(f'Finished dumping {subject}...')


