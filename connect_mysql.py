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
"""CREATE TABLE persons5
(id INT AUTO_INCREMENT PRIMARY KEY,
     surname VARCHAR(50) NOT NULL,
     name VARCHAR(50) NULL,
     patronymic VARCHAR(50) NULL,
     date_of_birth integer NULL,
     place_of_conscription VARCHAR(255) NULL,
     military_rank VARCHAR(255) NULL,
     date_of_death VARCHAR(50) NULL,
     location VARCHAR(255) NULL,
     died_in_battle boolean,
     loss boolean,
     pass_away boolean,
     died_of_wounds boolean,
     residence boolean,
     is_valid boolean
)
""")

# print("Table created successfully")
# mycursor.execute("SELECT * FROM persons5")
# myresult = mycursor.fetchall()
# print(myresult)
# for x in myresult:
#   print(x)
# mycursor.execute("""DROP TABLE persons;""")
#mycursor.execute("SHOW TABLES")

# sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
# val = ("John", "Highway 21")
# mycursor.execute(sql, val)

print("dfsdfdsf")
