from backend.supermarket import Supermarket
from psycopg2 import sql

supermarket = Supermarket()

def login_salesman():
    name = input("Write your name: ")
    password = input("Write your password")

    data_to_send = (name, password)

    query = sql.SQL("SELECT * FROM Salesman WHERE name = %s AND password = %s")

    if supermarket.fetch_one(query, data_to_send):
        return 0

    else:
        return 1
