import bs4
import requests
import json
import re
import time
from werkzeug.exceptions import Forbidden
def get_single_degrees(cid, index):
    url = f'https://www.handbook.unsw.edu.au/api/content/query/+contentType:course%20+course.implementation_year:2020%20-course.is_multi_award:1%20+course.parent_academic_org:{cid}%20+course.study_level:undergraduate%20/orderby/course.name%20asc'
    degrees = json.loads(requests.get(url).text)
    degreeJSON = []
    for degree in degrees['contentlets']:
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
    with open('../faculties.json', 'r') as f:
        local_degree = json.load(f)
    local_degree[index]['programs'] = degreeJSON
    with open('../faculties.json', 'w') as f:
        json.dump(local_degree, f, indent=4)

def get_double_degrees(cid, index):
    url = f'https://www.handbook.unsw.edu.au/rest/multi_award/field/parent_academic_org/id/*{cid}*/year/2020/level/undergraduate/limit/200/?json'
    degrees = json.loads(requests.get(url).text)
    degreeJSON = []
    for degree in degrees['contentlets']:
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
    with open('../faculties.json', 'r') as f:
        local_degree = json.load(f)
    local_degree[index]['programs'].extend(degreeJSON)
    with open('../faculties.json', 'w') as f:
        json.dump(local_degree, f, indent=4)

UGRAD_URL = 'https://www.handbook.unsw.edu.au/undergraduate/courses/2020/'
PGRAD_URL = 'https://www.handbook.unsw.edu.au/postgraduate/courses/2020/'

def write_enrolment_conditions(info, subjects, subject):
    if info is not None:
        conditions = info.find_all(class_='a-card-text m-toggle-text has-focus')
        subject['prereq'] = conditions[0].get_text().strip()
    with open('subjectinfo.json', 'w') as f:
        json.dump(subjects, f, indent=4)

def req_enrolment_conditions(subject, url):
    print(subject['name'], subject['code'])
    page = requests.get(url + f'{subject["code"]}')
    if page.status_code == 403:
        raise Forbidden('Restricted Access')
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    info = soup.find(id='SubjectConditions')
    return info

def find_all_conditions(url):
    with open('subjectinfo.json', 'r') as f:
        subjects = json.load(f)
    for faculty in subjects:
        for subject in subjects[faculty]:
            if isinstance(subject['prereq'], list):
                info = req_enrolment_conditions(subject, url)
                write_enrolment_conditions(info, subjects, subject)
                time.sleep(0.5)

def get_uac_code_double():
    with open('double_degrees.json', 'r') as f:
        degrees = json.load(f)

        for degree in degrees:
            page = requests.get(f'https://www.handbook.unsw.edu.au/undergraduate/programs/2020/{degree["code"]}')
            soup = bs4.BeautifulSoup(page.text, 'html.parser')
            text = soup.get_text()
            try:
                start = text.index('UAC Code') + len('UAC Code')
                hit_letter = False
                for index, char in enumerate(text[start:]):
                    if not hit_letter and char == ' ':
                        continue
                    if char == '\n' and not hit_letter:
                        hit_letter = True
                    elif char =='\n':
                        end = index + start
                        break
                code = text[start:end].strip()
                degree['uac_code'] = code
                print(str(degree['name']) + ' uac_code: ' + code)
                with open('double_degrees.json', 'w') as f:
                    json.dump(degrees, f, indent=4)
            except ValueError:
                print('No UAC Code found')
            time.sleep(1)
def handbook_prereq_parser():
    pass

find_all_conditions(PGRAD_URL)