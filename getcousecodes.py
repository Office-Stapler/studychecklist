import requests
import requests
from bs4 import BeautifulSoup
import re

url = "https://www.handbook.unsw.edu.au/FacultyOfArtsAndSocialSciences/browse?id=d7a56ceb4f0093004aa6eb4f0310c7ac"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')


'''
data = soup.find_all(id='singleCourseUndergraduate')
single = BeautifulSoup(str(data), 'html.parser')
data = single.find_all(class_="m-single-course-wrapper-browse")


print("single: ")
for course in data:
    search = re.search('left">(.*)</span' , str(course))
    string = search.group(1)
    print(string)
'''

print("")
data = soup.find_all(id='singleCourseUndergraduate')
single = BeautifulSoup(str(data), 'html.parser')
data = single.find_all(class_="a-browse-tile a-browse-tile--list regular-border-top")

print('single:')

for course in data:
    search = re.search('class="section">(.*)</div>' , str(course))
    string = search.group(1)
    print(string)


print("")
data = soup.find_all(id='multiCourseUndergraduate')
single = BeautifulSoup(str(data), 'html.parser')
data = single.find_all(class_="a-browse-tile a-browse-tile--list regular-border-top")

print('double:')

for course in data:
    search = re.search('class="section">(.*)</div>' , str(course))
    string = search.group(1)
    print(string)
