# To connect to postgreSQL
import psycopg2
from psycopg2 import sql
# To load the .env file
from dotenv import load_dotenv
# Importing OS commands to load the .env correctly
import os
# To use assyncronous commands
import asyncio

# loading .env
load_dotenv(".env",override = True)

class DBconnect:
    def __init__(self):
        # To avoid attribute errors
        self.conn = None
        self.cur = None

        # Throws an exception in case of connection failure
        try:
            self.conn = psycopg2.connect(
                dbname= os.getenv("db_name"),
                user=os.getenv("db_user"),
                password=os.getenv("db_password"),
                host=os.getenv("db_host"),
                port=os.getenv("db_port")
            )
        
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)

        # Tries to create a cursor to execute SQL commands
        try:
            self.cur = self.conn.cursor()

        except psycopg2.Error as error:
            print("Couldn't create the cursor")

    # ends connections with the database
    def end_connection(self):
        self.cur.close()
        self.conn.close()

    # Executes a SQL command
    def execute_command(self, sqlcommand, Params = None):
        self.cur.execute(sqlcommand, Params)
        self.conn.commit()

if __name__ == "__main__":
    db = DBconnect()

    query = sql.SQL("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)

    query2 = sql.SQL("""SELECT * FROM item;""")

    db.execute_command(query2)
    for item in db.cur.fetchall():
        print("+-------+")
        for items in item:
            if items == item[0]:
                print("|", items, "   |")
            else:
                print("|", items, "|")

    db.end_connection()