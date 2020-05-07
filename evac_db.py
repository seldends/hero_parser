import mysql.connector

from settings import MYSQL_PASSWORD

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=MYSQL_PASSWORD,
    database="mydatabase"
)


mycursor = mydb.cursor()


def create_evac_table():
    mycursor.execute(
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

    print("Table created successfully")


def clear_evac_table():
    sql_delete = """DELETE FROM `mydatabase`.`evac`;
    """
    sql_alter = """ALTER TABLE `mydatabase`.`evac` AUTO_INCREMENT = 1;
    """
    mycursor.execute(sql_delete)
    mycursor.execute(sql_alter)
    print("Table clear successfully")
    mydb.commit()


def drop_evac_table():
    mycursor.execute("DROP TABLE `mydatabase`.`evac`;")
    print("Table created successfully")


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
    mycursor.execute(sql, val)


def db_commit():
    mydb.commit()
    print("Изменения сохранены")


def print_evac_sql():
    sql_print = """SELECT FROM `mydatabase`.`evac`;
    """
    mycursor.execute(sql_print)


def main():
    pass


if __name__ == '__main__':
    main()
