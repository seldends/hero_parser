import mysql.connector

from settings import MYSQL_PASSWORD

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=MYSQL_PASSWORD,
    database="mydatabase"
)


mycursor = mydb.cursor()


# def create_db():
#     mycursor.execute("CREATE DATABASE mydatabase")
#     mydb.commit()


def create_persons_table():
    mycursor.execute(
    """CREATE TABLE perxlsx
    (id INT AUTO_INCREMENT PRIMARY KEY,
        surname VARCHAR(50) NOT NULL,
        name VARCHAR(50) NULL,
        patronymic VARCHAR(50) NULL,
        date_of_birth VARCHAR(50) NULL,
        place_of_conscription VARCHAR(255) NULL,
        military_rank VARCHAR(255) NULL,
        military_unit VARCHAR(255) NULL,
        date_of_death VARCHAR(50) NULL,
        location VARCHAR(255) NULL,
        fate VARCHAR(50) NULL,
        is_valid boolean
    )
    """)
    print("Table created successfully")


def create_evac_table():
    mycursor.execute(
    """CREATE TABLE evac
    (id INT AUTO_INCREMENT PRIMARY KEY,
        surname VARCHAR(50) NULL,
        name VARCHAR(50) NULL,
        patronymic VARCHAR(50) NULL,
        gender VARCHAR(1) NULL,
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
        search_fond integer NULL,
        search_inventory integer NULL,
        search_case integer NULL,
        search_list integer NULL,
        other_data VARCHAR(255) NULL
    )
    """)

    print("Table created successfully")


def clear_persons_table():
    mycursor.execute('DELETE FROM `mydatabase`.`perxlsx`;')
    mycursor.execute('ALTER TABLE `mydatabase`.`perxlsx` AUTO_INCREMENT = 1;')
    print("Table clear successfully")
    mydb.commit()


def count_persons_table():
    result = mycursor.execute('SELECT COUNT(*) FROM `mydatabase`.`perxlsx`;')
    print(result)


def save_persons(val):
    sql = """INSERT INTO perxlsx
        (surname, name, patronymic,
        date_of_birth, place_of_conscription, military_rank, military_unit,
        date_of_death, location, fate, is_valid)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    mycursor.execute(sql, val)


def save_evac(val):
    sql = """INSERT INTO evac
        (   surname, name, patronymic,
            gender, date_of_birth, before_evac_region,
            before_evac_district, before_evac_city, nationality,
            before_evac_place_of_work, before_evac_post,
            evac_district, evac_city, evac_with_company,
            evac_place_of_work, evac_post, settled_adress,
            search_archive, search_fond, search_inventory,
            search_case, search_list, other_data)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    mycursor.execute(sql, val)


def db_commit():
    mydb.commit()
    print("Изменения сохранены")


def main():
    pass


if __name__ == '__main__':
    main()
