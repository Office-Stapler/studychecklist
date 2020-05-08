import bs4
import requests
import json
import re
import time

def get_info_subject(subject):
    url = f'http://timetable.unsw.edu.au/2020/{subject}KENS.html'
    page = requests.get(url)
    if page.status_code == 404:
        url = f'http://timetable.unsw.edu.au/2020/{subject}COFA.html'
        page = requests.get(url)
        if page.status_code == 404:
            url = f'http://timetable.unsw.edu.au/2020/{subject}ADFA.html'
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

def get_single_degrees(cid):
    url = f'https://www.handbook.unsw.edu.au/api/content/query/+contentType:course%20+course.implementation_year:2020%20-course.is_multi_award:1%20+course.parent_academic_org:{cid}%20+course.study_level:undergraduate%20/orderby/course.name%20asc'
    degrees = json.loads(requests.get(url).text)
    degreeJSON = []
    for degree in degrees['contentlets']:
        #print(degree)
        try:
            degreeJSON.append({
                'uac_code': degree['uac_code'],
                'code': degree['code'],
                'name': degree['name']
            })
        except:
            degreeJSON.append({
                'uac_code': None,
                'code': degree['code'],
                'name': degree['name']
            })
    with open('single_degrees.json', 'r') as f:
        local_degree = json.load(f)
    local_degree.extend(degreeJSON)
    with open('single_degrees.json', 'w') as f:
        json.dump(local_degree, f, indent=4)

def get_double_degrees(cid):
    url = f'https://www.handbook.unsw.edu.au/rest/multi_award/field/parent_academic_org/id/*{cid}*/year/2020/level/undergraduate/limit/200/?json'
    degrees = json.loads(requests.get(url).text)
    degreeJSON = []
    for degree in degrees['contentlets']:
        #print(degree)
        try:
            degreeJSON.append({
                'uac_code': degree['uac_code'],
                'code': degree['code'],
                'name': degree['name']
            })
        except:
            degreeJSON.append({
                'uac_code': None,
                'code': degree['code'],
                'name': degree['name']
            })
    with open('double_degrees.json', 'r') as f:
        local_degree = json.load(f)
    local_degree.extend(degreeJSON)
    with open('double_degrees.json', 'w') as f:
        json.dump(local_degree, f, indent=4)

with open('double_degrees.json') as f:
    degrees = json.load(f)

degrees = sorted(degrees, key=lambda x: x['name'])
with open('double_degrees.json', 'w') as f:
    json.dump(degrees, f, indent=4)

""" with open('../faculties.json', 'r') as f:
    facs = json.load(f)
for fac in facs:
    get_double_degrees(fac['id'])
    print(f'Finished dumping {fac["name"]}')
    time.sleep(1) """