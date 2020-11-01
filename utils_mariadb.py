import mariadb
import sys
import numpy as np
import re

from settings import MARIADB_PASSWORD

try:
    conn = mariadb.connect(
        user="admin",
        password=MARIADB_PASSWORD,
        host="localhost",
        port=3306,
        database="hero_archiv"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cursor = conn.cursor()

def save_evac(val):
    sql = """INSERT INTO evac
        (   family_id, surname, name, patronymic,
            family_member, date_of_birth, before_evac_region,
            before_evac_district, before_evac_city, nationality,
            before_evac_place_of_work, before_evac_post,
            evac_district, evac_city, evac_with_company,
            evac_place_of_work, evac_post, settled_adress,
            search_archive, search_fond, search_inventory,
            search_case, search_list, other_data)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, val)


def save_data_bunch(data):
    query = """INSERT INTO evac
        (   family_id, surname, name, patronymic,
            family_member, date_of_birth, before_evac_region,
            before_evac_district, before_evac_city, nationality,
            before_evac_place_of_work, before_evac_post,
            evac_district, evac_city, evac_with_company,
            evac_place_of_work, evac_post, settled_adress,
            search_archive, search_fond, search_inventory,
            search_case, search_list, other_data)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.executemany(query, data)
    db_commit("В таблицу evac добавлено: " + str(len(data)) + " записей")


# Выбор данных по условию
def select_data_evac():
    # WHERE id > 54071
    # WHERE id < 18001
    # WHERE id < 18001 AND id > 54000
    # WHERE id > 18000 AND id < 36001
    # WHERE id > 36000 AND id < 54001
    sql_print = """SELECT family_id,surname, name, patronymic,
            family_member, date_of_birth, before_evac_region,
            before_evac_district, before_evac_city, nationality,
            before_evac_place_of_work, before_evac_post,
            evac_district, evac_city, evac_with_company,
            evac_place_of_work, evac_post, settled_adress,
            search_archive, search_fond, search_inventory,
            search_case, search_list, other_data FROM `hero_archiv`.`evac`;"""
    cursor.execute(sql_print)
    rows = cursor.fetchall()
    return rows


# Сохранение данных data = cur.fetchall() в sql с запросом
def save_data_to_sql_file(data):
    part = np.array_split(data, 2)
    print(len(part), type(part))
    for j in part:
        print(len(j), type(j))
    files_count = len(data) // 10000 + 1
    print(part)
    query = """INSERT INTO alexander_archiv_evac
        (family_id, surname, name, patronymic,
        family_member, date_of_birth, before_evac_region,
        before_evac_district, before_evac_city, nationality,
        before_evac_place_of_work, before_evac_post,
        evac_district, evac_city, evac_with_company,
        evac_place_of_work, evac_post, settled_adress,
        search_archive, search_fond, search_inventory,
        search_case, search_list, other_data)
        VALUES\n"""

    # print(files_count)
    # i = files_count
    # # while i > 0:
    i = 1
    for n_list in part:
        data1 = n_list.tolist()
        array_of_tuples = map(tuple, data1)
        data = tuple(array_of_tuples)
        with open("sql/output"+str(i)+".sql", "w") as text_file:
            data_str = str(data)
            data_str = data_str.replace('None', 'NULL')     # Замена None на Null
            data_str = data_str[1:]                         # Убирает ( в начале строки
            data_str = data_str[:-1]                        # Убирает ) в конце строки
            data_output = data_str
            data_output = data_str.replace(" ',", "',")
            # data_output = re.sub(r"[\s\'\,]", "',", data_str)
            ouput_str = query + data_output + ";"
            text_file.write(ouput_str)
            print("Запрос записан в файл")
            i += 1

# Очистка таблицы
def clear_table(table_name):
    sql_delete = "DELETE FROM " + table_name + ";"
    sql_alter = "ALTER TABLE " + table_name + " AUTO_INCREMENT = 1;"
    cursor.execute(sql_delete)
    cursor.execute(sql_alter)
    db_commit("Таблица " + table_name + " очищена")


# Применение изменений
def db_commit(message):
    conn.commit()
    print(message)
    # print("Изменения сохранены")


# Закрытие соединения
def close_connection():
    cursor.close()
    conn.close()
    print("закрытие соединения")