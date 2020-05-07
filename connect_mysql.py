import mysql.connector

from settings import MYSQL_PASSWORD

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=MYSQL_PASSWORD,
    database="mydatabase"
)


mycursor = mydb.cursor()


def create_persons_table():
    mycursor.execute(
        """CREATE TABLE IF NOT EXISTS acme_hero_heroes2s
        (   id INT AUTO_INCREMENT PRIMARY KEY,
            surname VARCHAR(50) NULL,
            name VARCHAR(50) NULL,
            patronymic VARCHAR(50) NULL,
            date_of_birth VARCHAR(50) NULL,
            place_of_conscription VARCHAR(255) NULL,
            military_rank VARCHAR(255) NULL,
            military_unit VARCHAR(255) NULL,
            date_of_death VARCHAR(50) NULL,
            location VARCHAR(255) NULL,
            fate VARCHAR(255) NULL,
            is_valid boolean)
        """)
    print("Table created successfully")


def drop_persons_table():
    mycursor.execute("DROP TABLE `mydatabase`.`acme_hero_heroes2s`;")
    print("Table created successfully")


def clear_persons_table():
    sql_delete = """DELETE FROM `mydatabase`.`acme_hero_heroes2s`;
    """
    sql_alter = """ALTER TABLE `mydatabase`.`acme_hero_heroes2s` AUTO_INCREMENT = 1;
    """
    mycursor.execute(sql_delete)
    mycursor.execute(sql_alter)
    print("Table clear successfully")
    mydb.commit()


def save_persons(val):
    sql = """INSERT INTO acme_hero_heroes2s
        (surname, name, patronymic,
        date_of_birth, place_of_conscription, military_rank, military_unit,
        date_of_death, location, fate, is_valid)
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    mycursor.execute(sql, val)


def db_commit():
    mydb.commit()
    print("Изменения сохранены")


def main():
    pass


if __name__ == '__main__':
    main()
