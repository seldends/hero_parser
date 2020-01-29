import re
from re import findall
from bs4 import BeautifulSoup
import psycopg2
import os


con = psycopg2.connect(
  database="postgres", 
  user="postgres", 
  password="jouzai", 
  host="127.0.0.1", 
  port="5432"
)

cur = con.cursor()


# Проверка на фио и дату рождения
def fio_and_bdate_verification(persons, fio_pattern):
    for person in persons:
        person_revision = re.findall(fio_pattern, person[0])
        person_revision = list(filter(None, person_revision))
 
        if len(person_revision) == 4:               # Проверка, если из 4х элементов
            try:                                        # и 4й число - значит все параметры есть
                int(person_revision[3])
                persons_fio_and_bdate.append(person)
            except:                                     # Если 4й не число - значит есть лишний текстовый параметр
                persons_not_valid_test.append(person)
        elif len(person_revision) == 3:             # Проверка, если из 3х элементов
            try:                                        # Если 3й число - значит нет отчества
                int(person_revision[2])
                persons_fi_and_bdate.append(person)
            except:                                     # Если 3й не число - нет даты рождения
                persons_fio.append(person) 
        elif len(person_revision) != 4:             # Оставшиеся варианты x<3 и x>4
            persons_not_valid_test.append(person)

    return persons_fio_and_bdate, persons_not_valid_test, persons_fi_and_bdate, persons_fio

# Есть ФИО и дата рождения 4\4
def fio_and_bdate_valid(persons, fio_pattern):
    for person in persons:
        data = re.findall(fio_pattern, person[0])
        data = list(filter(None, data))
        
        surname = data[0].capitalize()
        name = data[1].capitalize()
        patronymic = data[2].capitalize()
        birth_date = int(data[3])
        cur.execute("insert into persons (surname, name, patronymic, birth_date, other_data) values (%s, %s, %s, %s, %s)", (surname, name, patronymic, birth_date, person[1:]))
         

# Есть ФИО 3\4
def fio_valid(persons, fio_pattern):
    for person in persons:
        data = re.findall(fio_pattern, person[0])
        data = list(filter(None, data))
        
        surname = data[0].capitalize()
        name = data[1].capitalize()
        patronymic = data[2].capitalize()
        cur.execute("insert into persons (surname, name, patronymic,  other_data) values (%s, %s, %s, %s)", (surname, name, patronymic, person[1:]))


# Есть ФИ и дата рождения 3\4
def fi_and_bdate_valid(persons, fio_pattern):
    for person in persons:
        data = re.findall(fio_pattern, person[0])
        data = list(filter(None, data))
        
        surname = data[0].capitalize()
        name = data[1].capitalize()
        birth_date = int(data[2]) 
        cur.execute("insert into persons (surname, name, birth_date, other_data) values (%s, %s, %s,  %s)", (surname, name, birth_date, person[1:]))

# Сделать для persons_not_valid_test

a, b, c, d = 0, 0 ,0, 0

indir = r'C:\projects\parsing\html'
for root, dirs, filenames in os.walk(indir):
    for f in filenames:
        html_file = open(os.path.join(root, f),'r')
        print(f)
        contents = html_file.read()
        if contents:
            soup = BeautifulSoup(contents, 'html.parser')
            tags = soup.p.text
            data = tags.split("\n")
            # data = soup.p.text.split("\n")
            persons = []
            persons_not_valid_test = []
            persons_fio_and_bdate = []
            persons_fi_and_bdate = []
            persons_fio = []
            for line in data:
                if line and line != ' ':
                    result = re.split(r',', line)
                    persons.append(result)


            fio_pattern = r"\d{4}(?= г.р|)|[А-ЯЁ]* \([А-ЯЁ]*\)|[А-ЯЁ]*"

            persons_fio_and_bdate, persons_not_valid_test, persons_fi_and_bdate, persons_fio  = fio_and_bdate_verification(persons, fio_pattern)
            
            
            fio_and_bdate_valid(persons_fio_and_bdate, fio_pattern)
            fi_and_bdate_valid(persons_fi_and_bdate, fio_pattern)
            fio_valid(persons_fio, fio_pattern)


            a += len(persons_not_valid_test)
            b += len(persons_fio_and_bdate)
            c += len(persons_fi_and_bdate)
            d += len(persons_fio)
            
            # a = len(persons_not_valid_test) + len(persons_fio_and_bdate) + len(persons_fi_and_bdate) + len(persons_fio)
            # print(a)
            # print(len(persons))
            # print(len(persons_not_valid_test))
            # print(persons_not_valid_test)
            
            # print(persons_fio)
            # Посмотреть невалидных
            # print(persons_fio_and_bdate)
            # print(persons_valid)
            # Посмотреть число валидных\невалидных
            # print(len(persons_valid))
            # print(len(persons_not_valid))

print(f"not_valid_test {a}")
print(f"#fio_and_bdate fio_and_bdate {b}") 
print(f"#_fi_and_bdate {c}") 
print(f"#_fio {d}") 
print(f"hfghfghfgh {a+b+c+d}")
con.commit()      
con.close()
cur.close()



