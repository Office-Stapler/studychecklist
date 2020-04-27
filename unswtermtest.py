import requests
from bs4 import BeautifulSoup

course = input("enter course code: ")
url = f"https://www.handbook.unsw.edu.au/undergraduate/courses/2020/{course}/"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
data = soup.find_all('p')

for line in data:
    if 'Term' in str(line):
        terms = str(line)
    elif '':
        pass
    print(line)

des = str(data[0])
des = des[3:-4]
terms = "Terms available: " + terms[25:-4]
print(des)
print(terms)