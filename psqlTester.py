import psycopg

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