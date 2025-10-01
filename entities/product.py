from backend.supermarket import Supermarket
from psycopg2 import sql
supermarket = Supermarket()

def insert_item_product():
    name = input("Write the name of the product: ")
    value = float(input("Write the value of the product (EX: 20.5): "))
    quantity = int(input("Write the quantity in stock: "))

    query = sql.SQL("INSERT INTO Product (name, value, quantity) VALUES (%s, %s, %s)")

    data_to_send = (name, value, quantity)

    supermarket.execute_command(query, data_to_send)

def list_items_product():
    query1 = sql.SQL("SELECT COUNT(*) FROM Product;")

    query2 = sql.SQL("SELECT SUM(value) FROM Product;")

    query3 = sql.SQL("SELECT * FROM Product;")

    supermarket.execute_command(query1)

    result1 = supermarket.cur.fetchall()

    print("The quantity of items stored is: ",result1[0][0])
    
    supermarket.execute_command(query2)

    result2 = supermarket.cur.fetchall()

    print("The total sum of values in items is: ", result2[0][0])

    supermarket.execute_command(query3)

    result3 = supermarket.cur.fetchall()

    if result3:
        for i in result3:
            print(i)
        print("Items found")
    else:
        print("Items not found")

def search_by_id_product():
 
    id = input("Write the id of the product to be searched: ")

    data_to_send = (id,)

    query = sql.SQL("SELECT * FROM Product WHERE id = %s;")

    supermarket.execute_command(query, data_to_send)

    result = supermarket.cur.fetchall()

    if result:
        for i in result:
            print(i)
        print("Item found")
    else:
        print("Item not found")

def delete_item_product():
    name = input("Write the name of the product that will be deleted: ")

    data_to_send = (name,)

    query = sql.SQL("DELETE FROM Product WHERE name = %s;")

    supermarket.execute_command(query, data_to_send)
    print("Item deleted")

def product_crud_menu():

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
            insert_item_product()
        elif option == 2:
            list_items_product()
        elif option == 3:
            search_by_id_product()
        elif option == 4:
            delete_item_product()
        elif option == 5:
            return 0
        else:
            print("\n--> Invalid Option!")
            input("\n--> Press Enter...")
            product_crud_menu()
    except Exception as e:
        print(f"Erro: {e}")
        input("\n--> Press Enter...")
        product_crud_menu()