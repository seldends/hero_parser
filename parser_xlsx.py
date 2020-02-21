import pandas as pd
from test import time_test
from connect_mysql import create_persons_table, clear_persons_table, save_persons, db_commit


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

        # if date_of_birth is not None:
        #     try:
        #         date_of_birth = str(int(date_of_birth))

            

        # if date_of_birth is not None:
        #     date_of_birth = str(date_of_birth)
        #     if type(date_of_birth) == str:
        #         if date_of_birth == ' ':
        #             date_of_birth = None
        #         else:
        #             # print(date_of_birth)
        #             is_valid = False

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
        db_commit()


@time_test
def open_xlsx2(path_xlsx):
    xlsx = pd.ExcelFile(path_xlsx)

    df = xlsx.parse('Ц')
    df = df.where((pd.notnull(df)), None)
    pars(df)
    db_commit()


path_xlsx = 'xlsx/По буквам.xlsx'
path_test = 'xlsx/test.xlsx'
clear_persons_table()
# create_persons_table()

#open_xlsx(path_xlsx)
open_xlsx2(path_test)
