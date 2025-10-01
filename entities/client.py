from backend.supermarket import Supermarket
from psycopg2 import sql
supermarket = Supermarket()

def insert_client():
    name = input("Write the name of the client: ")
    password = input("Write the password of the client: ")

    query = sql.SQL("INSERT INTO Client (name, password) VALUES (%s, %s)")

    data_to_send = (name, password)

    supermarket.execute_command(query, data_to_send)

def list_client():
    query1 = sql.SQL("SELECT COUNT(*) FROM Client;")

    query3 = sql.SQL("SELECT id, name FROM Client;")

    supermarket.execute_command(query1)

    result1 = supermarket.cur.fetchall()

    print("The quantity of items stored is: ",result1[0][0])

    supermarket.execute_command(query3)

    result3 = supermarket.cur.fetchall()

    if result3:
        for i in result3:
            print(i)
        print("Items found")
    else:
        print("Items not found")

def search_by_id_client():
    id = input("Write the id of the client to be searched: ")

    data_to_send = (id,)

    query = sql.SQL("SELECT id, name FROM Client WHERE id = %s;")

    supermarket.execute_command(query, data_to_send)

    result = supermarket.cur.fetchall()

    if result:
        for i in result:
            print(i)
        print("Client found")
    else:
        print("Client not found")

def delete_client():
    name = input("Write the name of the client that will be deleted: ")

    data_to_send = (name,)

    query = sql.SQL("DELETE FROM Client WHERE name = %s;")

    supermarket.execute_command(query, data_to_send)
    print("Client deleted")

def login_client():
    name = input("Write your name: ")
    password = input("Write your password")

    data_to_send = (name, password)

    query = sql.SQL("SELECT * FROM Client WHERE name = %s AND password = %s")

    if supermarket.fetch_one(query, data_to_send):
        return 0

    else:
        return 1

def make_purchase():
    return

def clients_crud_menu():

    print(f"""{'-'*42}
    {'-'*18} MENU {'-'*18}
    {'-'*42}
    Cadastrar (1)
    Listar (2)
    Procurar por ID (3)
    Deletar (4)
    Voltar (5)""")

    try:
        option = int(input('Opção: '))
        if option == 1:
            insert_client()
        elif option == 2:
            list_client()
        elif option == 3:
            search_by_id_client()
        elif option == 4:
            delete_client()
        elif option == 5:
            return 0
        else:
            print("\n--> Invalid Option!")
            input("\n--> Press Enter...")
            clients_crud_menu()
    except Exception as e:
        print(f"Erro: {e}")
        input("\n--> Press Enter...")
        clients_crud_menu()

def close_connection():
    supermarket.end_connection()
    print("\n--> Connection closed.")