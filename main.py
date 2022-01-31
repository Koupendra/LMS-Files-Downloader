import requests
from bs4 import BeautifulSoup as BS
import sqlite3 as sql
import os
from shutil import rmtree

Session = requests.session()
with open("pwd.txt", "w") as f:
    username = input("Username: ")
    password = input("Password: ")
    f.writelines([username+"\n", password])

try:
    rmtree(os.getcwd() + '/My Courses')
except Exception as e:
    print(e)
    pass

courses_enrolled = []
number_of_courses = int(input("Number of courses: "))
for i in range(number_of_courses):
    courses_enrolled.append(input(f"Course code for course {i+1}: ").lower())

with open("course_details.db", "w") as f:
    pass

conn = sql.connect("course_details.db")
# noinspection SqlNoDataSourceInspection
conn.execute('''CREATE TABLE Courses(code TEXT NOT NULL, link TEXT NOT NULL UNIQUE, PRIMARY KEY (code))''')
conn.commit()

Session.post(url="https://lms.ssn.edu.in/login/index.php", data={'username': username, 'password': password})

resp = Session.get("https://lms.ssn.edu.in/")
soup = BS(resp.text, "html.parser")
tags = soup.find_all('a', {"class": "list-group-item list-group-item-action"})

for tag in tags:
    item = tag.findNext('span', {'class': "media-body"}).string.lower()
    for course in courses_enrolled:
        if course in item:
            # noinspection SqlResolve
            conn.execute('''INSERT INTO Courses(code, link) VALUES ("{}", "{}")'''.format(course, tag['href']))
            print(f"[+] {course.upper()} added...")
            break

conn.commit()
conn.close()
Session.close()
