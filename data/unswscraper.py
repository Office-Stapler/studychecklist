import bs4
import requests
import json
import re

def get_info_subject(subject):
    url = f'http://timetable.unsw.edu.au/2020/{subject}KENS.html'
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    subjects = soup.find_all('td', class_='formBody')
    ugrad = list(filter(lambda x: x != '', subjects[3].get_text().split('\n')))[3::]
    try:
        pgrad = list(filter(lambda x: x != '', subjects[5].get_text().split('\n')))[3::]
    except:
        pgrad = []
    try:
        research = list(filter(lambda x: x != '', subjects[7].get_text().split('\n')))[3::]
    except:
        research = []

    code = []
    title = []
    unit = []
    
    code.extend(ugrad[::3])
    title.extend(ugrad[1::3])
    unit.extend(ugrad[2::3])

    if pgrad != []:
        code.extend(pgrad[::3])
        title.extend(pgrad[1::3])
        unit.extend(pgrad[2::3])
    if research != []:
        code.extend(pgrad[::3])
        title.extend(research[1::3])
        unit.extend(research[2::3])
    final = list(zip(code, title, unit))

    with open('subjectinfo.json', 'r+') as f:
        courses = json.load(f)
        f.seek(0)
        courses.extend(final)
        json.dump(courses, f, indent=4)



with open('subjectarea.json', 'r') as f:
    subjects = json.load(f)

for title, subject in subjects:
    get_info_subject(subject)
    print(f'Finished dumping {subject}....')

