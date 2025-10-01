from backend.supermarket import Supermarket
from psycopg2 import sql
supermarket = Supermarket()

def close_connection():
    supermarket.end_connection()
    print("\n--> Connection closed.")

def insert_client():
    name = input("Write the name of the client: ")
    password = input("Write the password of the client: ")

    query = sql.SQL("INSERT INTO Client (name, password) VALUES (%s, %s)")

    data_to_send = (name, password)

    supermarket.execute_command(query, data_to_send)

def list_client():
    query1 = sql.SQL("SELECT COUNT(*) FROM Client;")

    query3 = sql.SQL("SELECT * FROM Client;")

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
            delete_item_client()
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