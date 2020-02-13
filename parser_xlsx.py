import pandas as pd
import mysql.connector

from settings import MYSQL_PASSWORD

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd=MYSQL_PASSWORD,
    database="mydatabase",
    auth_plugin="mysql_native_password"
)

mycursor = mydb.cursor()

#df = pd.read_excel('xlsx/part1.xlsx')
#df = pd.read_excel('xlsx/part2.xlsx')
df = pd.read_excel('xlsx/part3.xlsx')
df = df.where((pd.notnull(df)), None)

date_of_birth_pattern = r"\d{4}|\d{4}\s\(d{4}\)"


def pars(df):
    for i in df.index:
        name, patronymic, date_of_birth, date_of_death, location, fate = (None,)*6
        place_of_conscription, military_rank, military_unit = (None,)*3
        is_valid = True
        surname = df['Фамилия'][i]
        name = df['Имя'][i]
        patronymic = df['Отчество'][i]
        date_of_birth = df['Год рождения'][i]
        place_of_conscription = df['Место призыва'][i]
        military_rank = df['звание'][i]
        military_unit = df['Место службы'][i]
        date_of_death = df['Дата смерти'][i]
        location = df['Место проживания (захоронения)'][i]
        fate = df['Судьба'][i]
        if type(date_of_birth) == str:
            if date_of_birth == ' ':
                date_of_birth = None
            else:
                print(date_of_birth)
                is_valid = False
        sql = """INSERT INTO perxlsx
        (surname, name, patronymic,
        date_of_birth, place_of_conscription, military_rank, military_unit,
        date_of_death, location, fate, is_valid)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        val = (
            surname, name, patronymic,
            date_of_birth, place_of_conscription, military_rank, military_unit,
            date_of_death, location, fate, is_valid
            )

        mycursor.execute(sql, val)


pars(df)
mydb.commit()
print(mycursor.rowcount, "Записи сохранены")
