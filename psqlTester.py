import psycopg
from datetime import date
from dotenv import load_dotenv 
import os

load_dotenv()


USERNAME = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB = os.getenv("POSTGRES_DB")
HOST = "localhost"
PORT = "5432"

TABLE = 'expenses'


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


def insert_receipt(expense, cost, date=date.today()):
    try:
        with psycopg.connect(conninfo) as conn:
            with conn.cursor() as cur:
                cur.execute(f"INSERT INTO {TABLE} (Date, ToE, Amount) VALUES (%s, %s, %s)", (date, expense, cost))
                return True
    except Exception as e:
        print(f"Failed to insert: {e}")
        return False

"""Make sure to pass in as a list, this is just in case use passes in multiple we are prepared for that"""
def delete_receipt(ids: list):
    try:
        with psycopg.connect(conninfo) as conn:
            with conn.cursor() as cur:
                for id in ids:
                    cur.execute(f'DELETE FROM {TABLE} WHERE receiptid = {id}')
                return True
    except Exception as e:
        print(f'Failed to remove row: {e}')
        return False
    
delete_receipt([1,3])