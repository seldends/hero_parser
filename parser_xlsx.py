import pandas as pd
from utils import time_test
from utils_db_mysql import save_persons, db_commit, close_connection
from utils_db_mysql import create_table_persons as create_table
from utils_db_mysql import clear_table
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


# Открытие и запись всей книги
@time_test
def open_book(path_xlsx):
    xlsx = pd.ExcelFile(path_xlsx)
    for sheet in xlsx.sheet_names:
        print(sheet)
        df = xlsx.parse(sheet)
        df = df.where((pd.notnull(df)), None)
        pars(df)
    db_commit("Данные записаны")


# Открытие и запись отдельного листа
@time_test
def open_list(path_xlsx, list_name):
    xlsx = pd.ExcelFile(path_xlsx)
    df = xlsx.parse(list_name)
    df = df.where((pd.notnull(df)), None)
    pars(df)
    db_commit("Данные записаны")


def main():
    path_xlsx = 'xlsx/По буквам.xlsx'
    table = "`mydatabase`.`acme_hero_heroes2s`"

    create_table()              # Создание таблицы, если не существует
    clear_table(table)          # Очистка таблицы и сброс id
    open_book(path_xlsx)        # Обработка всей книги
    close_connection()          # Закрытие соединения
    #pass


if __name__ == '__main__':
    main()
