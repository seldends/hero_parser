import pandas as pd
from test import time_test
from connect_mysql import clear_persons_table, save_persons, db_commit


date_of_birth_pattern = r"\d{4}|\d{4}\s\(d{4}\)"


@time_test
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
        military_rank = df['Звание'][i]
        military_unit = df['Место службы'][i]
        date_of_death = df['Дата смерти'][i]
        location = df['Место проживания (захоронения)'][i]
        fate = df['Судьба'][i]
        if type(date_of_birth) == str:
            if date_of_birth == ' ':
                date_of_birth = None
            else:
                #print(date_of_birth)
                is_valid = False

        val = (
            surname, name, patronymic,
            date_of_birth, place_of_conscription, military_rank, military_unit,
            date_of_death, location, fate, is_valid
            )
        save_persons(val)


xlsx = pd.ExcelFile('xlsx/По буквам.xlsx')

clear_persons_table()

for sheet in xlsx.sheet_names:
    print(sheet)
    df = xlsx.parse(sheet)
    df = df.where((pd.notnull(df)), None)
    pars(df)

db_commit()
