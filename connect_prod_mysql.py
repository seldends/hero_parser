import mysql.connector

from settings import MYSQL_PASSWORD

mydb = mysql.connector.connect(
    host="10.0.1.225",
    user="archiv",
    passwd="34r6IcL0FGiPt0Wo{",
    port=3306
)

mycursor = mydb.cursor()


mycursor.execute("SHOW TABLES")

for x in mycursor:
    print(x)

print('Ok')

