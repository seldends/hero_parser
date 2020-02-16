import re
import os
from connect_mysql import save_persons, db_commit
from bs4 import BeautifulSoup


persons = []
persons_data = []

fio_pattern = r"[А-ЯЁ]* \([А-ЯЁ]*\)|[А-ЯЁ]*"
date_of_birth_pattern = r"\d{4}(?= г.р|)"
place_of_conscription_pattern = r"РВК|ГВК|р-н|с\.|г\.(\s|)[А-ЯЁ]"   # подумать
location_pattern = r"р-н|с\.|г\.(\s|)[А-ЯЁ]|не\sустановлено"
military_rank_pattern = r"ст-на|с-т|ряд\.|ст\. л-т|гв\. с-т|с-т|мл\. л-т|ефр"

died_in_battle_pattern = r"(?<=погиб\s)\d{2}\,{0,1}\.{0,1}\d{2}\,{0,1}\.{0,1}\d{2,4}|(?<=погибла\s)\d{2}\,{0,1}\.{0,1}\d{2}\,{0,1}\.{0,1}\d{2,4}"
pass_away_pattern = r"(?<=умер\s)\d{2}\,{0,1}\.{0,1}\d{2}\,{0,1}\.{0,1}\d{2,4}|(?<=умерла\s)\d{2}\,{0,1}\.{0,1}\d{2}\,{0,1}\.{0,1}\d{2,4}"
died_of_wounds_pattern = r"(?<=умер\sот\sран\s)\d{2}\,{0,1}\.{0,1}\d{2}\,{0,1}\.{0,1}\d{2,4}|(?<=умер\sот\sран\s)\d{2}\,{0,1}\.{0,1}\d{2}\,{0,1}\.{0,1}\d{2,4}"
loss_pattern = r"(?<=пропал\sбез\sвести\s)\d{2}\,{0,1}\.{0,1}\d{2}\,{0,1}\.{0,1}\d{2,4}|(?<=пропала\sбез\sвести\s)\d{2}\,{0,1}\.{0,1}\d{2}\,{0,1}\.{0,1}\d{2,4}"
died_in_captivity_pattern = r"(?<=погиб\sв\sплену\s)\d{2}\,{0,1}\.{0,1}\d{2}\,{0,1}\.{0,1}\d{2,4}|(?<=погибла\sв\sплену\s)\d{2}\,{0,1}\.{0,1}\d{2}\,{0,1}\.{0,1}\d{2,4}"
released_from_captivity_pattern = r"(?<=попал\sв\sплен\s)\d{2}\,{0,1}\.{0,1}\d{2}\,{0,1}\.{0,1}\d{2,4}|(?<=попала\sв\sплен\s)\d{2}\,{0,1}\.{0,1}\d{2}\,{0,1}\.{0,1}\d{2,4}"
residence_pattern = r"проживал\sпосле\sвойны|проживала\sпосле\sвойны"

fate_dict = {
    died_in_battle_pattern: 'погиб',
    loss_pattern: "пропал без вести",
    pass_away_pattern: "умер",
    died_of_wounds_pattern: "умер от ран",
    died_in_captivity_pattern: "погиб в плену",
    released_from_captivity_pattern: "попал в плен, освобожден",
    residence_pattern: "проживал после войны"
}


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


# Проверяет в элементе, и возвращает ФИО
def check_fio(data):
    fio = re.findall(fio_pattern, data)
    if fio:
        fio = list(filter(None, fio))
        surname = fio[0].capitalize()
        try:
            name = fio[1].capitalize()
        except IndexError:
            name = None
        try:
            patronymic = fio[2].capitalize()
        except IndexError:
            patronymic = None
        return surname, name, patronymic
    return None, None, None


# Проверяет в элементе, и возвращает результат
def check_dbirth(data):
    result = re.findall(date_of_birth_pattern, data)
    if result:
        return result[0]
    return None


# Проверяет в списке, и возвращает элемент
def check_rank(data):
    for element in data:
        result = re.findall(military_rank_pattern, element)
        if result:
            unit = re.sub(military_rank_pattern, "", element.strip())
            return result[0], unit
    return None, None


# Придумать как сделать проверку
def check_conscription(data):
    for element in data:
        result = re.findall(place_of_conscription_pattern, element)
        if result:
            return element.strip()
    return None


# Проверяет в списке, и возвращает дату, место, судьбу
def check_fate(data):
    for element in data:
        for pattern, value_fate in fate_dict.items():
            result = re.findall(pattern, element)
            if result:
                if pattern == released_from_captivity_pattern:
                    return result[0], None, fate_dict[pattern]
                elif pattern == residence_pattern:
                    r = element.rfind("после войны")
                    return None, element[r+11:], fate_dict[pattern]
                try:
                    next_element = data[data.index(element)+1]
                    test = re.findall(location_pattern, next_element)
                    if test:
                        return result[0], next_element.strip(), fate_dict[pattern]
                except IndexError:
                    return result[0], None, fate_dict[pattern]
    return None, None, "не указано"


def pars(persons):
    for person in persons:
        name, patronymic, date_of_birth, date_of_death, location, fate = (None,)*6
        place_of_conscription, military_rank, military_unit = (None,)*3
        is_valid = False

        surname, name, patronymic = check_fio(person[0])
        date_of_birth = check_dbirth(person[0])
        place_of_conscription = check_conscription(person[1:3])
        military_rank, military_unit = check_rank(person[1:])
        date_of_death, location, fate = check_fate(person[1:])

        val = (
            surname, name, patronymic,
            date_of_birth, place_of_conscription, military_rank, military_unit,
            date_of_death, location, fate, is_valid
            )

        save_persons(val)


folder = r'/mnt/c/projects/parsing/html/htest'
make_persons(folder)

for person in persons_data:
    result = re.split(r',', person)
    persons.append(result)
print(len(persons_data))
print(len(persons))

pars(persons)

db_commit()
