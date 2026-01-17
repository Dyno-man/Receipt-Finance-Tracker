import psycopg
from datetime import date

USERNAME = "test"
PASSWORD = "db_123"
DB = "example"
HOST = "localhost"
PORT = "5432"


conninfo = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}'

try:
    with psycopg.connect(conninfo) as conn:
        print("DJ KHALID")
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            print(cur.fetchone())
except Exception as e:
    print(f"Connection failed : {e}")


print(date.today())

try:
    with psycopg.connect(conninfo) as conn:
        print("We're in")

        with conn.cursor() as cur:

            cur.execute("INSERT INTO expenses (Date, ToE, Amount) VALUES (%s, %s, %s)", (date.today(), "Grocery", 100))

            cur.execute("SELECT * FROM expenses;")
except Exception as e:
    print(f'Failed: {e}')