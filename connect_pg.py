import psycopg2

from settings import PG_PASSWORD

con = psycopg2.connect(
  database="postgres",
  user="postgres",
  password=PG_PASSWORD,
  host="localhost",
  port="5432"
)


def create_db(conn):
    cur = conn.cursor()
    cur.execute("CREATE DATABASE mydb")
    print("DB created successfully")


def create_table(conn):
    cur = conn.cursor()
    cur.execute('''CREATE TABLE persons1  (
     id SERIAL,
     surname VARCHAR(50) NOT NULL,
     name VARCHAR(50) NULL,
     patronymic VARCHAR(50) NULL,
     date_of_birth integer NULL,
     place_of_conscription VARCHAR(255) NULL,
     military_rank VARCHAR(255) NULL,

     date_of_death VARCHAR(50) NULL,
     date_of_loss boolean,
     date_of_pass_away boolean,
     date_died_of_wounds boolean,

     place of stay VARCHAR(255) NULL,
     place_of_residence boolean,
     place_of_death boolean,
     place_of_pass_away boolean,
     place_died_of_wounds boolean
     )
     ''')
    print("Table created successfully")
    conn.commit()
    cur.close()


create_table(con)


con.close()
