import pandas as pd
from test import time_test
from connect_mysql import save_persons, db_commit
from connect_mysql import create_persons_table as create_table
from connect_mysql import clear_persons_table as clear_table
import datetime


@time_test
def pars(df):
    test_list = []
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



        # if date_of_birth is not None:
        #     try:
        #         date_of_birth = str(int(date_of_birth))
        if patr is not None:
            patronymic = patr.upper()

        if type(date_of_death) == datetime.datetime:
            date_of_death = date_of_death.strftime('%d.%m.%Y')

        if date_of_birth is not None:
            if type(date_of_birth) == str:
                if date_of_birth == ' ':
                    print('dsfsdfsdf')
                    date_of_birth = None
                else:
                    is_valid = False
            if type(date_of_birth) == float:
                date_of_birth = int(date_of_birth)
            date_of_birth = str(date_of_birth)

        # if date_of_birth is not None:
        #     if type(date_of_birth) == float:
        #         date_of_birth = int(date_of_birth)
        #     date_of_birth = str(date_of_birth)

        val = (
            surname, name, patronymic,
            date_of_birth, place_of_conscription, military_rank, military_unit,
            date_of_death, location, fate, is_valid
            )
        #test_list.append(val)
        
        #save_persons(val)

    #save_persons(val)
    return test_list


@time_test
def open_xlsx2(path_xlsx):
    xlsx = pd.ExcelFile(path_xlsx)

    df = xlsx.parse('Э')
    df = df.where((pd.notnull(df)), None)
    pars(df)
    db_commit()


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
def open_xlsx3(path_xlsx):
    xlsx = pd.ExcelFile(path_xlsx)

    df = xlsx.parse('А потеряшки')
    df = df.where((pd.notnull(df)), None)
    test_list = pars(df)
    print(test_list)

    #f= open("test.txt","w+")
    #f.write(str(test_list))

    #db_commit()

@time_test
def open_xlsx4(path_xlsx):
    
    df = pd.read_excel(path_xlsx, sheet_name=None)
    #df = df.where((pd.notnull(df)), None)
    #df = df.fillna(None)

    pars(df)
    db_commit()

path_test = 'xlsx/a2.xlsx'
path_xlsx = 'xlsx/По буквам.xlsx'
clear_table()
# create_table

#open_xlsx2(path_test)
#open_xlsx(path_xlsx)
open_xlsx3(path_test)
#open_xlsx4(path_xlsx)
