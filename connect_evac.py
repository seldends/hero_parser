import mysql.connector

from settings import MYSQL_PASSWORD

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=MYSQL_PASSWORD,
    database="mydatabase"
)


mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE mydatabase")

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
