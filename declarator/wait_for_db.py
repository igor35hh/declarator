import psycopg2
from time import sleep

connect_str = "dbname='declarator' user='django' host='postgresdb' port='5432' " + \
              "password='12345678'"

while True:
    try:
        conn = psycopg2.connect(connect_str)
    except psycopg2.OperationalError as e:
        if "authentication failed" in e.args[0]:
            print("Postgres is ready.  Launching site.")
            break
        else:
            print("Waiting for postgres...", e.args[0])
            sleep(1)