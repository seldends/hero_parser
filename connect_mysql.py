import mysql.connector

from settings import MYSQL_PASSWORD

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd=MYSQL_PASSWORD,
    database="mydatabase",
    auth_plugin="mysql_native_password"
)

mycursor = mydb.cursor()

#mycursor.execute("CREATE DATABASE mydatabase")

mycursor.execute(
"""CREATE TABLE persons6
(id INT AUTO_INCREMENT PRIMARY KEY,
surname VARCHAR(50) NOT NULL,
name VARCHAR(50) NULL,
patronymic VARCHAR(50) NULL,
date_of_birth VARCHAR(50) NULL,
place_of_conscription VARCHAR(255) NULL,
military_rank VARCHAR(255) NULL,
date_of_death VARCHAR(50) NULL,
date_of_loss VARCHAR(50) NULL,
date_of_pass_away VARCHAR(50) NULL,
date_died_of_wounds VARCHAR(50) NULL,
place_of_residence VARCHAR(255) NULL,
place_of_death VARCHAR(255) NULL)
place_of_pass_away VARCHAR(255) NULL,
place_died_of_wounds VARCHAR(255) NULL
)
""")

print("Table created successfully")
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

#print(mydb) 