import json
import requests
from bs4 import BeautifulSoup
import re
import time
from multiprocessing import Pool

def htmlfromsite(code):
    url = (f"https://www.handbook.unsw.edu.au/undergraduate/programs/2020/{code}?browseByFaculty={faculty}&")
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    data = soup.find_all(class_="o-ai-overview__h1")
    search = re.search('module-title">(.*)</span>' , str(data))
    string = search.group(1)
    return string

if __name__ == '__main__':
    time_start = time.time()
    with open('faculties.json', 'r') as f:
        facultiesData = json.load(f)

    singles = facultiesData[0]['programs']
    doubles = facultiesData[0]['double']
    faculty = facultiesData[0]['name']

    with Pool(10) as p:
        singles = p.map(htmlfromsite, singles)

    with Pool(10) as p:
        doubles = p.map(htmlfromsite, doubles)

    print(singles)
    print(doubles)

    print("time: "+ str(time.time()- time_start))


