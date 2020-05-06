import json
import requests
from bs4 import BeautifulSoup
import re

with open('faculties.json', 'r') as f:
    faculties = json.load(f)



url = 'https://www.handbook.unsw.edu.au/search?&ct=course&study_level=ugrd&multi_award=1'
page = requests.get(url).text

soup = BeautifulSoup(page, 'html.parser')
print(soup)

