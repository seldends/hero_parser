import pandas as pd
import numpy as np

from utils import time_test
# from utils_db_mysql import db_commit, close_connection
# from utils_db_mysql import save_evac as save_table
# from utils_db_mysql import save_data_bunch
# from utils_db_mysql import create_table_evac as create_table
# from utils_db_mysql import clear_table
# from utils_db_mysql import drop_table
# from utils_db_mysql import save_query_to_file

from utils_mariadb import db_commit, close_connection, save_data_bunch
from utils_mariadb import save_evac, clear_table
from utils_mariadb import select_data_evac, save_data_to_sql_file


#! выбирать 2е число
# family_id_global = 40316
family_id_global = 69523
# family_id_global = 53964
# 1й файл 19031 11769
# 2й файл 54071	37997
# 3й файл 55621	38780
# 6й файл 59235	40316


def check(column, i, df):
    data = df[column][i]
    if type(data) == np.int64:
        return int(data)
    elif type(data) == float:
        return str(data).replace(".0", "")
    elif type(data) == str:
        return data.strip()
    if data == '-':
        data = None

    return data


@time_test
def pars(df):
    all_dict = []

    for i in df.index:
        global family_id_global
        family_id = None
        family_id_temp = None
        name = None
        patronymic = None
        family_member = None
        date_of_birth = None
        before_evac_region = None
        before_evac_district = None
        before_evac_city = None
        nationality = None
        before_evac_place_of_work = None
        before_evac_post = None
        evac_district = None
        evac_city = None
        evac_with_company = None
        evac_place_of_work = None
        evac_post = None
        settled_address = None
        search_archive = None
        search_fond = None
        search_inventory = None
        search_case = None
        search_list = None
        other_data = None

        family_id_temp = df['номер'][i]

        if family_id_temp:
            family_id_global += 1

        family_id = family_id_global

        surname = str(df['фамилия'][i]).strip()
        name = check('имя', i, df)
        patronymic = check('отчество', i, df)
        family_member = check('отношение', i, df)
        date_of_birth = check('год рождения', i, df)
        before_evac_region = check('область1', i, df)
        before_evac_district = check('район1', i, df)
        before_evac_city = check('город1', i, df)
        nationality = check('национальность', i, df)
        before_evac_place_of_work = check('предприятие', i, df)
        before_evac_post = check('должность1', i, df)
        evac_district = check('район2', i, df)
        evac_city = check('город2', i, df)
        evac_with_company = check('организация', i, df)
        evac_place_of_work = check('место работы', i, df)
        evac_post = check('должность2', i, df)
        settled_address = check('адрес', i, df)
        search_archive = check('архив', i, df)
        search_fond = check('фонд', i, df)
        search_inventory = check('опись', i, df)
        search_case = check('дело', i, df)
        search_list = check('лист', i, df)
        other_data = check('примечание', i, df)

        val = (
            family_id, surname, name, patronymic,
            family_member, date_of_birth, before_evac_region,
            before_evac_district, before_evac_city, nationality,
            before_evac_place_of_work, before_evac_post,
            evac_district, evac_city, evac_with_company,
            evac_place_of_work, evac_post, settled_address,
            search_archive, search_fond, search_inventory,
            search_case, search_list, other_data
        )
        try:
            save_evac(val)
        except:
            print(val)
        #all_dict.append(val)

    #save_data_bunch(all_dict)


@time_test
def open_xlsx(path_xlsx):
    xlsx = pd.ExcelFile(path_xlsx)
    test_list = xlsx.sheet_names
    # test_list.pop(0)
    # test_list.pop(0)
    print(test_list)

    for sheet in test_list:
        print(sheet)
        df = xlsx.parse(sheet)
        df = df.where((pd.notnull(df)), None)
        pars(df)


def main():
    path_xlsx = 'xlsx/evac30.10.2020.xlsx'
    table = "`hero_archiv`.`evac`"
    # table = "evac"

    # create_table()              # Создание таблицы, если не существует
    clear_table(table)          # Очистка таблицы и сброс id
    open_xlsx(path_xlsx)        # Обработка всей книги
    db_commit("Данные записаны")
    

    # Сохранение данных в файл
    data = select_data_evac()
    save_data_to_sql_file(data)
    close_connection()          # Закрытие соединения
    #pass


if __name__ == '__main__':
    main()