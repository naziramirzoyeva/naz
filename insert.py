import csv 
import psycopg2

conn = psycopg2.connect(
    dbname = "phonebook",
    user = "postgres",
    password = "aiko2502",
    host = "localhost",
    port = "5432"
)

cur = conn.cursor()

with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        cur.execute(
            "INSERT INTO phonebook (first_name, last_name, phone_number) VALUES (%s, %s, %s)",
            row
        )
conn.commit()
cur.close()
conn.close()
print("Data imported succesfully")