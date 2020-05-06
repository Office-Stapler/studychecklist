import json
import requests
from bs4 import BeautifulSoup
import re

with open('faculties.json', 'r') as f:
    facultiesData = json.load(f)

#for faculties in facultiesData:
url = f"https://www.handbook.unsw.edu.au/{facultiesData[0]['name']}/browse?id={facultiesData[0]['id']}"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
print("")
#print(f"        {faculties['name']}:")


data = soup.find_all(id='singleCourseUndergraduate')
single = BeautifulSoup(str(data), 'html.parser')
data = single.find_all(class_="m-single-course-wrapper-browse")

print("single: ")
for course in data:
    search = re.search('left">(.*)</span' , str(course))
    string = search.group(1)
    print(string)

print("")
data = soup.find_all(id='multiCourseUndergraduate')
single = BeautifulSoup(str(data), 'html.parser')
data = single.find_all(class_="a-browse-tile a-browse-tile--list regular-border-top")

for line in data:
    print("")
    print("")
    print("")
    print(line)

print('double:')
for course in data:
    print(course)
    search = re.search('Program(.*), ' , str(course))
    string = search.group(1)
    print(string)


