import pandas as pd
import numpy as np

from test import time_test
from utils_db_mysql import db_commit, close_connection
from utils_db_mysql import save_evac as save_table
from utils_db_mysql import save_data_bunch
from utils_db_mysql import create_table_evac as create_table
from utils_db_mysql import clear_table
from utils_db_mysql import drop_table
from utils_db_mysql import save_query_to_file

import datetime

#! выбирать 2е число
family_id_global = 0
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

        surname = df['фамилия'][i]
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
        # print(type(evac_place_of_work))
        evac_post = check('должность2', i, df)
        settled_address = check('адрес', i, df)
        search_archive = check('архив', i, df)
        search_fond = check('фонд', i, df)
        search_inventory = check('опись', i, df)
        search_case = check('дело', i, df)
        search_list = check('лист', i, df)
        other_data = check('примечание', i, df)

        # val_test = [
        #     surname, name, patronymic,
        #     family_member, date_of_birth, before_evac_region,
        #     before_evac_district, before_evac_city, nationality,
        #     before_evac_place_of_work, before_evac_post,
        #     evac_district, evac_city, evac_with_company,
        #     evac_place_of_work, evac_post, settled_address,
        #     search_archive, search_fond,
        #     search_list, other_data
        #     ]

        # for i in val_test:
        #     if i:
        #         i = str(i).strip()

        # dict_replace = [search_case, search_inventory]
        # for j in dict_replace:
        #     j = str(j).replace(".0", "")

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
        all_dict.append(val)
        #save_table(val)
    # print(len(all_dict))
    # print(all_dict)
    save_data_bunch(all_dict)


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


#path_xlsx = 'xlsx/evac3.xlsx'
path_xlsx = 'xlsx/evac_all.xlsx'


table = "`mydatabase`.`evac`"
drop_table(table)
create_table()
clear_table(table)
open_xlsx(path_xlsx)
db_commit("Данные записаны")
close_connection()
#save_query_to_file()
