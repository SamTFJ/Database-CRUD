from backend.supermarket import Supermarket
from psycopg2 import sql
from backend.crud import CRUD
from entities.client import Client
from entities.product import Product
from entities.purchase import Purchase
from entities.sale_items import SaleItems
from entities.sales import Sale
from entities.salesman import Salesman

if __name__ == "__main__":
    type = None
    supermarket = Supermarket()
    
    while type != "1" and type != "2":
        type = input("Are you a Client (1) or a Salesman (2)?\n")

    if type == "1":
        option1 = input("Do you have an account? \n   1- YES\n   2- NO\n")
        
        if option1 == "1":
            name = input("Write your name: ")
            password = input("Write your password: ")

            data_to_send = (name, password)
            query1 = sql.SQL("SELECT * FROM Client WHERE name = %s AND password = %s;")
            confirmation = supermarket.fetch_one(query1, data_to_send)
        
            if confirmation:
                crud = CRUD(type=type)
                crud.run()

            else:
                type = None
        
        elif option1 == "2":
            name = input("Write your name: ")
            password = input("Write your password: ")
            
            client = Client()

            client.set_name(name=name)
            client.set_password(password=password)

            data_to_send = (client.client[0], client.client[1], client.client[2])

            query = sql.SQL("INSERT INTO Client (name, password, purchases) VALUES (%s, %s, %s)")
            supermarket.execute_command(query,data_to_send)

    if type == "2":
        option1 = input("Do you have an account?\n   1- YES\n   2- NO\n")
        
        if option1 == "1":
            name = input("Write your name:")
            password = input("Write your password")

            data_to_send = (name, password)
            query1 = sql.SQL("SELECT * FROM Salesman WHERE name = %s AND password = %s;")
            confirmation = supermarket.fetch_one(query1, data_to_send)
        
            if confirmation:
                crud = CRUD(type=type)
                crud.run()

            else:
                type = None
        
        elif option1 == "2":
            name = input("Write your name")
            password = input("Write your password")
            
            salesman = Salesman()

            salesman.set_name(name=name)
            salesman.set_password(password=password)

            data_to_send = (salesman.salesman[0], salesman.salesman[1], salesman.salesman[2])

            query = sql.SQL("INSERT INTO Salesman (name, password, number) VALUES (%s, %s, %s)")
            supermarket.execute_command(query,data_to_send)