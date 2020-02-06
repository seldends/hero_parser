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
"""CREATE TABLE persons
(id INT AUTO_INCREMENT PRIMARY KEY,
     surname VARCHAR(50) NOT NULL,
     name VARCHAR(50) NULL,
     patronymic VARCHAR(50) NULL,
     date_of_birth integer NULL,
     place_of_conscription VARCHAR(255) NULL,
     military_rank VARCHAR(255) NULL,
     date_of_death VARCHAR(50) NULL,
     location VARCHAR(255) NULL,
     fate VARCHAR(50) NULL,
     is_valid boolean
)
""")

print("Table created successfully")
