from backend.supermarket import Supermarket
from psycopg2 import sql

supermarket = Supermarket()

def login_salesman():
    name = input("Write your name: ")
    password = input("Write your password: ")

    data_to_send = (name, password)

    query = sql.SQL("SELECT * FROM Salesman WHERE name = %s AND password = %s")

    if supermarket.fetch_one(query, data_to_send) != None:
        return True

    else:
        return False

def insert_salesman():
    name = input("Write the name of the salesman: ")
    password = input("Write the password of the salesman: ")

    query = sql.SQL("INSERT INTO Salesman (name, password) VALUES (%s, %s)")

    data_to_send = (name, password)

    supermarket.execute_command(query, data_to_send)

def list_salesman():
    query1 = sql.SQL("SELECT COUNT(*) FROM Salesman;")

    query3 = sql.SQL("SELECT id, name FROM Salesman;")

    supermarket.execute_command(query1)

    result1 = supermarket.cur.fetchall()

    print("The quantity of Salesman stored is: ",result1[0][0])

    supermarket.execute_command(query3)

    result3 = supermarket.cur.fetchall()

    if result3:
        for i in result3:
            print(i)
        print("Salesman found")
    else:
        print("Salesman not found")

def search_by_id_salesman():
    id = input("Write the id of the salesman to be searched: ")

    data_to_send = (id,)

    query = sql.SQL("SELECT id, name FROM Salesman WHERE id = %s;")

    supermarket.execute_command(query, data_to_send)

    result = supermarket.cur.fetchall()

    if result:
        for i in result:
            print(i)
        print("Client found")
    else:
        print("Client not found")

def delete_salesman():
    name = input("Write the name of the salesman that will be deleted: ")

    data_to_send = (name,)

    query = sql.SQL("DELETE FROM Salesman WHERE name = %s;")

    supermarket.execute_command(query, data_to_send)
    print("Salesman deleted")

def salesman_crud_menu():

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
            insert_salesman()
        elif option == 2:
            list_salesman()
        elif option == 3:
            search_by_id_salesman()
        elif option == 4:
            delete_salesman()
        elif option == 5:
            return 0
        else:
            print("\n--> Invalid Option!")
            input("\n--> Press Enter...")
            salesman_crud_menu()
    except Exception as e:
        print(f"Erro: {e}")
        input("\n--> Press Enter...")
        salesman_crud_menu()