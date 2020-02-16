import pandas as pd
import numpy as np
from connect_mysql import save_evac, db_commit


df = pd.read_excel('evac.xlsx')
df = df.where((pd.notnull(df)), None)

date_of_birth_pattern = r"\d{4}|\d{4}\s\(d{4}\)"


def check(column, i):
    data = df[column][i]
    if type(data) == np.int64:
        return int(data)
    if data == '-':
        data = None
    return data


def pars_evac(df):
    for i in df.index:
        name = None
        patronymic = None
        gender = None
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

        surname = df['фамилия'][i]
        name = check('имя', i)
        patronymic = check('отчество', i)
        gender = check('пол', i)
        date_of_birth = check('год рождения', i)
        before_evac_region = check('область1', i)
        before_evac_district = check('район1', i)
        before_evac_city = check('город1', i)
        nationality = check('национальность', i)
        before_evac_place_of_work = check('предприятие', i)
        before_evac_post = check('должность1', i)
        evac_district = check('район2', i)
        evac_city = check('город2', i)
        evac_with_company = check('организация', i)
        evac_place_of_work = check('место работы', i)
        evac_post = check('должность2', i)
        settled_adress = check('адрес', i)
        search_archive = check('архив', i)
        search_fond = check('фонд', i)
        search_inventory = check('опись', i)
        search_case = check('дело', i)
        search_list = check('лист', i)
        other_data = check('примечание', i)

        # #print(surname, name)

        val = (
            surname, name, patronymic,
            gender, date_of_birth, before_evac_region,
            before_evac_district, before_evac_city, nationality,
            before_evac_place_of_work, before_evac_post,
            evac_district, evac_city, evac_with_company,
            evac_place_of_work, evac_post, settled_adress,
            search_archive, search_fond, search_inventory,
            search_case, search_list, other_data
            )

        save_evac(val)


pars_evac(df)
db_commit()
