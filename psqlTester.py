import psycopg
from datetime import date
from dotenv import load_dotenv 
import os
import random

load_dotenv()


USERNAME = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB = os.getenv("POSTGRES_DB")
HOST = "localhost"
PORT = "5432"

TABLE = 'expenses'


conninfo = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}'

# try:
#     with psycopg.connect(conninfo) as conn:
#         print("DJ KHALID")
#         with conn.cursor() as cur:
#             cur.execute("SELECT version();")
#             print(cur.fetchone())
# except Exception as e:
#     print(f"Connection failed : {e}")


# print(date.today())

# try:
#     with psycopg.connect(conninfo) as conn:
#         print("We're in")

#         with conn.cursor() as cur:

#             cur.execute("INSERT INTO expenses (Date, ToE, Amount) VALUES (%s, %s, %s)", (date.today(), "Grocery", 100))

#             cur.execute("SELECT * FROM expenses;")
# except Exception as e:
#     print(f'Failed: {e}')

"""
This function does exactly what it says, it will insert receipt data into the psql db
expense => This is expense type
cost => This is the total cost
date => This is the date and time of when the receipt was uploaded
"""
def insert_receipt(expense: str, cost: int, date=date.today()):
    try:
        with psycopg.connect(conninfo) as conn:
            with conn.cursor() as cur:
                cur.execute(f"INSERT INTO {TABLE} (Date, ToE, Amount) VALUES (%s, %s, %s)", (date, expense, cost))
                return True
    except Exception as e:
        print(f"Failed to insert: {e}")
        return False


"""
This functino does exactly what it says, it will remove receipt data in the psql db
ids => This is a list of ids that we want to remove
"""
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
    

"""
Want to make a general purpose query for sorting, so I guess that means i want 4 functions.
I will be sorting by Date, Type of Expense, and Amount
I think sorting by IDs won't really be useful for a frontend scenario so this is how i want to do it for now
"""

"""
For functions with the sort var you have three options for passing values
-1 => is data < data
0 => is data = data
1 => is data > data
"""

"""
This function will return receipts uploaded before, after, or equal to what the user requests
date => is a date object
sort => int
"""
def search_date(date: date, sort: int) -> bool:
    try:
        with psycopg.connect(conninfo) as conn:
            with conn.cursor() as cur:
                if sort == -1:
                    cur.execute(f'SELECT date, toe, amount FROM {TABLE} WHERE date < {date}')    
                elif sort == 0:
                    cur.execute(f'SELECT date, toe, amount FROM {TABLE} WHERE date = {date}')
                else:
                    cur.execute(f'SELECT date, toe, amount FROM {TABLE} WHERE date > {date}')
                return True
    except Exception as e:
        print(f'Failed to remove row: {e}')
        return False
"""
This function will return receipts uploaded before, after, or equal to what the user requests
date => is a date object
sort => int
"""
def search_toe(toe) -> bool:
    try:
        with psycopg.connect(conninfo) as conn:
            with conn.cursor() as cur:
                cur.execute(f'SELECT date, toe, amount FROM {TABLE} WHERE toe = {toe}')
                return True
    except Exception as e:
        print(f'Failed to remove row: {e}')
        return False -1
"""
This function will return receipts uploaded before, after, or equal to what the user requests
date => is a date object
sort => int
"""
def search_amount(amount: int, sort: int) -> bool:
    try:
        with psycopg.connect(conninfo) as conn:
            with conn.cursor() as cur:
                if sort == -1:
                    cur.execute(f'SELECT date, toe, amount FROM {TABLE} WHERE amount < {amount}')    
                elif sort == 0:
                    cur.execute(f'SELECT date, toe, amount FROM {TABLE} WHERE amount = {amount}')
                else:
                    cur.execute(f'SELECT date, toe, amount FROM {TABLE} WHERE amount > {amount}')
                
                for record in cur:
                    print(record)
                return True

    except Exception as e:
        print(f'Failed to remove row: {e}')
        return False

"""
This function inserts random test data
date => is a date object
sort => int
"""
def insert_random_data():
    categories = ["Grocery", "Automobile", "Other", "Wasteful"]
    information = []

    for _ in range(random.randint(10, 50)):
        information.append([date.today(), categories[random.randint(0,3)], random.randint(1, 1000)])
     
    for item in information:
        insert_receipt(item[1], item[2], item[0])

"""
This function will return receipts uploaded before, after, or equal to what the user requests
date => is a date object
sort => int
"""
def get_all_data():
    try:
        with psycopg.connect(conninfo) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {TABLE}")

                for record in cur:
                    print(record)

                return cur
    except Exception as e:
        print(f"Failed to grab data: {e}")
        return False