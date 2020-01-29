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
date_of_death_pattern = r"(?<=погиб )\d\d.\d\d.\d\d|(?<=погибла )\d\d.\d\d.\d\d"
date_of_pass_away_pattern = r"(?<=умер )\d\d.\d\d.\d\d|(?<=умерла )\d\d.\d\d.\d\d"
date_died_of_wounds_pattern = r"(?<=умер от ран )\d\d.\d\d.\d\d|(?<=умер от ран )\d\d.\d\d.\d\d"
date_of_loss_pattern = r"(?<=пропал без вести )\d\d.\d\d.\d\d|(?<=пропала без вести )\d\d.\d\d.\d\d"
place_of_residence_pattern = r"проживал после войны|проживала после войны"
place_of_conscription_pattern = r"РВК" #тест
military_rank_pattern = r"ст-на|с-т|ряд.|ст. л-т|гв. с-т|с-т|мл. л-т|ефр"



# Придумать как можно лучше
def make_persons(directory): 
    for root, dirs, filenames in os.walk(directory):
        for f in filenames:
            html_file = open(os.path.join(root, f),'r')
            #print(f)
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


# Проверяет в списке, и возвращает следующий элемент 
# Элемен "место смерти" идет после "даты смерти"

def check_data_next(pattern, data):
    for element in data:
        result = re.findall(pattern, element)
        if result:
            try:
                return data[data.index(element)+1].strip()
            except IndexError:
                return None
    return None


def pars(persons):
    for person in persons:

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

        date_of_death = check_list(date_of_death_pattern, person[1:])
        date_of_loss = check_list(date_of_loss_pattern, person[1:])
        date_of_pass_away = check_list(date_of_pass_away_pattern, person[1:])
        date_died_of_wounds = check_list(date_died_of_wounds_pattern, person[1:])

        #  Подумать как сделать
        place_of_residence = check_data(place_of_residence_pattern, person[1:])  

        place_of_death = check_data_next(date_of_death_pattern, person[1:])
        place_of_pass_away = check_data_next(date_of_pass_away_pattern, person[1:])
        place_died_of_wounds = check_data_next(date_died_of_wounds_pattern, person[1:])


        sql = """INSERT INTO persons6
        (surname, name, patronymic, 
        date_of_birth, place_of_conscription, military_rank, 
        date_of_death, date_of_loss, date_of_pass_away, date_died_of_wounds, 
        place_of_residence, place_of_death, place_of_pass_away, place_died_of_wounds) 
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        val = (
            surname, name, patronymic, 
            date_of_birth, place_of_conscription, military_rank, 
            date_of_death, date_of_loss, date_of_pass_away, date_died_of_wounds, 
            place_of_residence, place_of_death, place_of_pass_away, place_died_of_wounds
            )

        mycursor.execute(sql, val)


folder = r'C:\projects\parsing\html'
make_persons(folder)

for person in persons_data:
    result = re.split(r',', person)
    persons.append(result)
print(len(persons_data))
print(len(persons))
pars(persons)


mydb.commit()
print(mycursor.rowcount, "record inserted.")