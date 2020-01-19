import psycopg2

con = psycopg2.connect(
  database="postgres", 
  user="postgres", 
  password="postgres", 
  host="127.0.0.1", 
  port="5432"
)

cur = con.cursor()

cur.execute('''CREATE TABLE persons  
     (id SERIAL,  
     surname VARCHAR(50) NOT NULL,
     name VARCHAR(50) NOT NULL,
     patronymic VARCHAR(50) NULL, 
     birth_date integer NULL,
     other_data VARCHAR(255) NOT NULL)
     ;''')

# cur.execute('''CREATE TABLE per_not_valid 
#      (id SERIAL,
#      surname VARCHAR(50) NOT NULL,
#      name VARCHAR(50) NOT NULL,
#      patronymic VARCHAR(50) NULL, 
#      birth_date integer NULL,
#      other_data VARCHAR(255) NOT NULL)
#      ;''')

print("Table created successfully")

con.commit() 
con.close()
cur.close()