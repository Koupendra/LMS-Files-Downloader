import requests
from bs4 import BeautifulSoup as BS
import sqlite3 as sql
import os
from shutil import rmtree

filetype = {"spreadsheet-24": ".xlsx",
            "document-24": ".docx",
            "pdf-24": ".pdf",
            "powerpoint-24": ".pptx"}

Session = requests.session()

with open("pwd.txt") as f:
    username = f.readline().rstrip()
    password = f.readline().rstrip()

Session.post(url="https://lms.ssn.edu.in/login/index.php", data={'username': username, 'password': password})

conn = sql.connect('course_details.db')

# noinspection SqlResolve
try:
    rmtree(os.getcwd() + '/My Courses')
except Exception as e:
    print(e)
    pass
os.mkdir('My Courses')


for course, link in conn.execute('''SELECT * from Courses'''):
    os.mkdir(f"My Courses/{course.upper()}")
    resp = Session.get(link)
    soup = BS(resp.text, 'html.parser')
    sections = soup.find_all('div', {'class': 'content'})

    j = 1
    for section in sections:
        head = section.findNext('h3')
        os.mkdir(f"My Courses/{course.upper()}/{j}_{head.text}")
        contents = section.find_all('li', {'class': 'activity resource modtype_resource'})

        i = 1
        for content in contents:
            ext = content.findNext('img', {'class': "iconlarge activityicon"})['src'].split("/")[-1]
            if ext not in filetype:
                continue
            url = content.findNext('a')['href']
            title = content.findNext('span', {'class': 'instancename'}).text
            filename = f'{i}_{title}'
            open(f"My Courses/{course.upper()}/{j}_{head.text}/{filename+filetype[ext]}", "wb").write(
                Session.get(url, allow_redirects=True).content)
            i += 1
        j += 1

    pass

conn.close()
Session.close()
