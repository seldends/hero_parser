import mysql.connector
import psycopg2

from settings import PG_PASSWORD
from settings import MYSQL_PASSWORD

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=MYSQL_PASSWORD,
    database="mydatabase"
)

# connection = psycopg2.connect(
#     database="test1",
#     user="postgres",
#     password=PG_PASSWORD,
#     host="localhost",
#     port="5432"
# )


cursor = connection.cursor()


# Создание таблицы
def create_table_evac():
    #! id для mysql id INT AUTO_INCREMENT PRIMARY KEY
    #! id для postgres id SERIAL
    cursor.execute(
        """CREATE TABLE evac
        (   id INT AUTO_INCREMENT PRIMARY KEY,
            family_id integer NULL,
            surname VARCHAR(50) NULL,
            name VARCHAR(50) NULL,
            patronymic VARCHAR(50) NULL,
            family_member VARCHAR(50) NULL,
            date_of_birth VARCHAR(50) NULL,
            before_evac_region VARCHAR(255) NULL,
            before_evac_district VARCHAR(255) NULL,
            before_evac_city VARCHAR(255) NULL,
            nationality VARCHAR(255) NULL,
            before_evac_place_of_work VARCHAR(255) NULL,
            before_evac_post VARCHAR(255) NULL,
            evac_district VARCHAR(255) NULL,
            evac_city VARCHAR(255) NULL,
            evac_with_company VARCHAR(255) NULL,
            evac_place_of_work VARCHAR(255) NULL,
            evac_post VARCHAR(255) NULL,
            settled_adress VARCHAR(255) NULL,
            search_archive VARCHAR(255) NULL,
            search_fond VARCHAR(50) NULL,
            search_inventory VARCHAR(50) NULL,
            search_case VARCHAR(50) NULL,
            search_list VARCHAR(50) NULL,
            other_data VARCHAR(255) NULL
        )
        """)
    db_commit("Таблица evac создана")


# Удаление таблицы
def drop_table(table_name):
    cursor.execute("DROP TABLE " + table_name + ";")
    db_commit("Таблица " + table_name + " удалена")


# Очистка таблицы
def clear_table(table_name):
    sql_delete = "DELETE FROM " + table_name + ";"
    sql_alter = "ALTER TABLE " + table_name + " AUTO_INCREMENT = 1;"
    cursor.execute(sql_delete)
    cursor.execute(sql_alter)
    db_commit("Таблица " + table_name + " очищена")


# Добавление данных в таблицу
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


# Удаление данных из таблицы с условием
def delete_from_evac():
    sql_print = """DELETE FROM `mydatabase`.`evac` WHERE id > 54071;"""
    cursor.execute(sql_print)
    db_commit("Данные из таблицы evac удалены")


# Применение изменений
def db_commit(message):
    connection.commit()
    print(message)
    # print("Изменения сохранены")


# Закрытие соединения
def close_connection():
    cursor.close()
    connection.close()
    print("закрытие соединения")


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
            search_case, search_list, other_data FROM `mydatabase`.`evac` WHERE id > 18000 AND id < 36001;"""
    cursor.execute(sql_print)
    rows = cursor.fetchall()
    return rows


# Сохранение данных data = cur.fetchall() в sql с запросом
def save_data_to_sql_file(data):
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
    with open("sql/output.sql", "w") as text_file:
        data_str = str(data)
        data_str = data_str.replace('None', 'NULL')     # Замена None на Null
        data_str = data_str[1:]                         # Убирает ( в начале строки
        data_str = data_str[:-1]                        # Убирает ) в конце строки

        ouput_str = query + data_str + ";"
        text_file.write(ouput_str)
        print("Запрос записан в файл")


# Сохранение данных с листа excel запросом с множественными значениями
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
    # data_str = str(data)
    # data_str = data_str.replace('None', 'NULL')     # Замена None на Null
    # data_str = data_str[1:]                         # Убирает [ в начале строки
    # data_str = data_str[:-1]                        # Убирает ] в конце строки
    # value = data_str
    cursor.executemany(query, data)
    db_commit("В таблицу evac добавлено: " + str(len(data)) + "записей")


# Запись данных в файл из таблицы
def save_query_to_file():
    data = select_data_evac()
    save_data_to_sql_file(data)


def main():
    # create_table()
    # drop_table()
    # print_evac_sql()
    # delete_from_family()
    # clear_article_table()
    # con.close()
    pass


if __name__ == '__main__':
    main()
