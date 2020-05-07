import pandas as pd
import numpy as np

from test import time_test
from evac_db import db_commit
from evac_db import save_evac as save_table
from evac_db import create_evac_table as create_table
from evac_db import clear_evac_table as clear_table
from evac_db import drop_evac_table as drop_table
import datetime

family_id_global = 0


def check(column, i, df):
    data = df[column][i]
    if type(data) == np.int64:
        return int(data)
    if data == '-':
        data = None
    return data


@time_test
def pars(df):
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
        settled_adress = None
        search_archive = None
        search_fond = None
        search_inventory = None
        search_case = None
        search_list = None
        other_data = None

        family_id_temp = df['номер'][i]
        if not family_id_temp and i > 0:
            j = 1
            while not family_id_temp:
                family_id_temp = df['номер'][i-j]
                j += 1
        if family_id_global:
            family_id = family_id_global + family_id_temp
        else:
            family_id = family_id_temp
        try:
            df['номер'][i+1]
        except KeyError:
            family_id_global = family_id_temp

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
        evac_post = check('должность2', i, df)
        settled_adress = check('адрес', i, df)
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
            evac_place_of_work, evac_post, settled_adress,
            search_archive, search_fond, search_inventory,
            search_case, search_list, other_data
        )

        save_table(val)


@time_test
def open_xlsx(path_xlsx):
    xlsx = pd.ExcelFile(path_xlsx)
    for sheet in xlsx.sheet_names:
        print(sheet)
        df = xlsx.parse(sheet)
        df = df.where((pd.notnull(df)), None)
        pars(df)

# def print_sql():


path_xlsx = 'xlsx/evac2.xlsx'

# drop_table()
# create_table()
clear_table()

open_xlsx(path_xlsx)
db_commit()
