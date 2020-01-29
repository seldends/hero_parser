import psycopg2

from settings import PG_PASSWORD

con = psycopg2.connect(
  database="postgres", 
  user="postgres", 
  password=PG_PASSWORD, 
  host="127.0.0.1", 
  port="5432"
)

cur = con.cursor()

cur.execute('''CREATE TABLE persons6  (
     id SERIAL,  
     surname VARCHAR(50) NOT NULL,
     name VARCHAR(50) NULL,
     patronymic VARCHAR(50) NULL, 
     date_of_birth integer NULL,
     place_of_conscription VARCHAR(255) NULL,
     military_rank VARCHAR(255) NULL,
     date_of_death VARCHAR(50) NULL,
     date_of_loss VARCHAR(50) NULL,
     date_of_pass_away VARCHAR(50) NULL,
     date_died_of_wounds VARCHAR(50) NULL,
     place_of_residence VARCHAR(255) NULL,
     place_of_death VARCHAR(255) NULL,
     place_of_pass_away VARCHAR(255) NULL,
     place_died_of_wounds VARCHAR(255) NULL
     )
     ''')

print("Table created successfully")

con.commit() 
con.close()
cur.close()