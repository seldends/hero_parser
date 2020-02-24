import pandas as pd
from test import time_test
from connect_mysql import save_persons, db_commit
from connect_mysql import create_persons_table as create_table
from connect_mysql import clear_persons_table as clear_table
import datetime


@time_test
def pars(df):
    for i in df.index:
        name, patronymic, date_of_birth, date_of_death, location = (None,)*5
        fate, place_of_conscription, military_rank, military_unit = (None,)*4
        is_valid = True

        surname = df['Фамилия'][i]
        name = df['Имя'][i]
        patr = df['Отчество'][i]
        date_of_birth = df['Год рождения'][i]
        place_of_conscription = df['Место призыва'][i]
        military_rank = df['Звание'][i]
        military_unit = df['Место службы'][i]
        date_of_death = df['Дата смерти'][i]
        location = df['Место проживания (захоронения)'][i]
        fate = df['Судьба'][i]

        if patr is not None:
            patronymic = patr.upper()

        if type(date_of_death) == datetime.datetime:
            date_of_death = date_of_death.strftime('%d.%m.%Y')

        if date_of_birth is not None:
            if type(date_of_birth) == float:
                date_of_birth = int(date_of_birth)
            date_of_birth = str(date_of_birth)

        val = (
            surname, name, patronymic,
            date_of_birth, place_of_conscription, military_rank, military_unit,
            date_of_death, location, fate, is_valid
            )
        save_persons(val)


@time_test
def open_xlsx(path_xlsx):
    xlsx = pd.ExcelFile(path_xlsx)
    for sheet in xlsx.sheet_names:
        print(sheet)
        df = xlsx.parse(sheet)
        df = df.where((pd.notnull(df)), None)
        pars(df)


path_xlsx = 'xlsx/По буквам.xlsx'

create_table()
clear_table()

open_xlsx(path_xlsx)
db_commit()
