import re
import os
import mysql.connector
from bs4 import BeautifulSoup

from settings import MYSQL_PASSWORD

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd=MYSQL_PASSWORD,
    database="mydatabase",
    auth_plugin="mysql_native_password"
)

mycursor = mydb.cursor()


persons = []
persons_data = []

fio_pattern = r"[А-ЯЁ]* \([А-ЯЁ]*\)|[А-ЯЁ]*"
date_of_birth_pattern = r"\d{4}(?= г.р|)"

died_in_battle_pattern = r"(?<=погиб\s)\d\d.\d\d.\d\d|(?<=погибла\s)\d\d.\d\d.\d\d"
pass_away_pattern = r"(?<=умер\s)\d\d.\d\d.\d\d|(?<=умерла\s)\d\d.\d\d.\d\d"
died_of_wounds_pattern = r"(?<=умер от ран\s)\d\d.\d\d.\d\d|(?<=умер от ран\s)\d\d.\d\d.\d\d"
loss_pattern = r"(?<=пропал без вести\s)\d\d.\d\d.\d\d|(?<=пропала без вести\s)\d\d.\d\d.\d\d"

# died_in_battle_pattern = r"((?<=погиб )|(?<=погибла ))\d\d.\d\d.\d\d"
# pass_away_pattern = r"((?<=умер\s)|(?<=умерла\s))\d\d.\d\d.\d\d"
# died_of_wounds_pattern = r"((?<=умер от ран\s)|(?<=умер от ран\s))\d\d.\d\d.\d\d"
# loss_pattern = r"((?<=пропал без вести\s)|(?<=пропала без вести\s))\d\d.\d\d.\d\d"

residence_pattern = r"проживал после войны|проживала после войны"
place_of_conscription_pattern = r"РВК" #тест

military_rank_pattern = r"ст-на|с-т|ряд.|ст. л-т|гв. с-т|с-т|мл. л-т|ефр"


# Придумать как можно лучше
def make_persons(directory):
    for root, dirs, filenames in os.walk(directory):
        for f in filenames:
            html_file = open(os.path.join(root, f), 'r', encoding='cp1251')
            print(f)
            soup = BeautifulSoup(html_file.read(), 'html.parser')
            tags = soup.p.text
            data = tags.split("\n")

            for line in data:
                if line and line != ' ':
                    line = line.strip()
                    condition = re.match(r"^[А-ЯЁ]{4,}", line)
                    if condition:
                        persons_data.append(line)
                    else:
                        persons_data[-1] = persons_data[-1]+line

    return persons_data


# Т.К. ФИО и ДР почти всегда находятся в 1м элементе списка, то искать их следует там
# Остальные данные могут быть в произвольном элементе списка, поэтому поиск идет по всем элементам, кроме 1го

# Проверяет в элементе, и возвращает список ФИО
def check_fio(pattern, data):
    result = re.findall(pattern, data)
    if result:
        result = list(filter(None, result))
        return result
    return None


# Проверяет в элементе, и возвращает результат
# "дата рождения" находится в 1м элементе списка

def check_one(pattern, data):
    result = re.findall(pattern, data)
    if result:
        return result[0]
    return None


# Проверяет в списке, и возвращает результат
# Среди всех  элементов ищутся даты смерти

def check_list(pattern, data):
    for element in data:
        result = re.findall(pattern, element)
        if result:
            return result[0]
    return None


# Проверяет в списке, и возвращает элемент
# Если находит часть из звания - то возращает весь элемент

def check_data(pattern, data):
    for element in data:
        result = re.findall(pattern, element)
        if result:
            return element.strip()
    return None


def check_residence(pattern, data):
    for element in data:
        result = re.findall(pattern, element)
        if result:
            r = element.rfind("после войны")
            return element[r+11:].strip(), True
    return None, False
# Проверяет в списке, и возвращает следующий элемент
# Элемен "место смерти" идет после "даты смерти"


def check_date(pattern_date, data):
    for element in data:
        result = re.findall(pattern_date, element)
        if result:
            try:
                return result[0], data[data.index(element)+1].strip(), True
            except IndexError:
                return result[0], None, True
    return None, None, False


def pars(persons):
    for person in persons:

        date_of_death = None
        location = None

        died_in_battle = False
        loss = False
        pass_away = False
        died_of_wounds = False
        residence = False

        is_valid = False

        fio = check_fio(fio_pattern, person[0])

        surname = fio[0].capitalize()
        try:
            name = fio[1].capitalize()
        except IndexError:
            name = None
        try:
            patronymic = fio[2].capitalize()
        except IndexError:
            patronymic = None

        date_of_birth = check_one(date_of_birth_pattern, person[0])
        place_of_conscription = check_data(place_of_conscription_pattern, person[1:])
        military_rank = check_data(military_rank_pattern, person[1:])

        date_died_in_battle, place_died_in_battle, died_in_battle = check_date(died_in_battle_pattern, person[1:])
        date_of_loss, place_of_loss, loss = check_date(loss_pattern, person[1:])
        date_of_pass_away, place_of_pass_away, pass_away = check_date(pass_away_pattern, person[1:])
        date_died_of_wounds, place_died_of_wounds, died_of_wounds = check_date(died_of_wounds_pattern, person[1:])
        place_of_residence, residence = check_residence(residence_pattern, person[1:])


        if died_in_battle:
            date_of_death = date_died_in_battle
            location = place_died_in_battle
        elif loss:
            date_of_death = date_of_loss
            location = place_of_loss
        elif pass_away:
            date_of_death = date_of_pass_away
            location = place_of_pass_away
        elif died_of_wounds:
            date_of_death = date_died_of_wounds
            location = place_died_of_wounds
        elif residence:
            location = place_of_residence

        sql = """INSERT INTO persons4
        (surname, name, patronymic,
        date_of_birth, place_of_conscription, military_rank,
        date_of_death, location,
        died_in_battle, loss, pass_away,
        died_of_wounds, residence,
        is_valid)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        val = (
            surname, name, patronymic,
            date_of_birth, place_of_conscription, military_rank,
            date_of_death, location,
            died_in_battle, loss, pass_away,
            died_of_wounds, residence,
            is_valid
            )

        mycursor.execute(sql, val)


folder = r'/mnt/c/projects/parsing/html'
make_persons(folder)

for person in persons_data:
    result = re.split(r',', person)
    persons.append(result)
print(len(persons_data))
print(len(persons))
pars(persons)

mydb.commit()
print(mycursor.rowcount, "record inserted.")
