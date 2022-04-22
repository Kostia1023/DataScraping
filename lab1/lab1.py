from bs4 import BeautifulSoup
from requests import get
from json import dump
from re import fullmatch,match
from sqlite3 import connect

def get_staff_name(list):
    for el in list:
        name = match(r'/ua/person/',el['href'])
        if name is not None:
            return el.getText()

BASE_URL = 'https://www.univer.kharkov.ua'
url = BASE_URL + '/ua/departments'
print(url)

page = get(url)
soup = BeautifulSoup(page.content, 'html.parser')
faculties = []

i= 0

connections = connect("lab2.db")
cursor = connections.cursor()

for el in soup.find(class_="left_box_kz").find(class_="left_menu").find(class_="main_nav_menu").find_all('li'):
    el_a = el.find('a')
    href_facult = fullmatch(r'/[a-z]+/[a-z]+/[a-z]+', el_a['href'])
    if href_facult is not None:

        departments = []
        try:
            chair = el.find(class_="disp_none").find(class_="disp_none").find_all('a')
        except Exception:
            departments = None
        else:
            #departments = [el.getText() for el in chair]
            for el in chair:
                departments.append(el.getText())
                cursor.execute(
                    "INSERT INTO departments (name, faculty) VALUES (?, ?)",
                    [el.getText(), i]
                )

        page_staff = get(BASE_URL + href_facult.group(0) + '/' + href_facult.group(0)[16:] + '_staff')
        soup_staff = BeautifulSoup(page_staff.content, 'html.parser')
        staff_names = [f'{el.find("strong").getText() } {get_staff_name(el.find_all("a"))}' for el in soup_staff.find(class_="academ_kontact").find_all(class_='clear')]
        for el in staff_names:
            cursor.execute(
                "INSERT INTO staffs (name, faculty) VALUES (?, ?)",
                [el, i]
            )
        faculty = {
            "name": el_a.getText(),
            "url": href_facult.group(0),
            "departments": departments,
            "staffs": staff_names
        }
        cursor.execute(
            "INSERT INTO faculties (name, url) VALUES (?, ?)",
            [faculty['name'],faculty["url"]]
        )
        faculties.append(faculty)
        i+=1
    connections.commit()

connections.close()

with open("lab1.json", "w", encoding="utf-8") as json_file:
    dump(faculties, json_file, ensure_ascii=False, indent=4)

