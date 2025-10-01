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
    password = input("Write your password: ")

    data_to_send = (name, password)

    query = sql.SQL("SELECT * FROM Client WHERE name = %s AND password = %s")

    if supermarket.fetch_one(query, data_to_send) != None:
        return True
    else:
        return False

def make_purchase():
    carrinho = []
    total_compra = 0

    name = input("Write your name: ")
    password = input("Write your password: ")

    data_to_send = (name, password)

    query = sql.SQL("SELECT id FROM Client WHERE name = %s AND password = %s")

    if supermarket.fetch_one(query, data_to_send) != None:
        print("Login feito com sucesso!")

        client_id = int(input("Write your client id: "))

        # Loop para adicionar produtos ao carrinho
        while True:
            try:
                # Mostra alguns produtos para facilitar
                print("\nProdutos disponíveis:")
                available_products = supermarket.fetch_all("SELECT id, name, value, quantity FROM Product WHERE quantity > 0 LIMIT 20;")
                for p in available_products:
                    print(f"  ID: {p[0]}, Nome: {p[1]}, Preço: R${p[2]:.2f}, Estoque: {p[3]}")

                product_id = int(input("\nDigite o ID do produto a adicionar (ou 0 para finalizar): "))
                if product_id == 0:
                    break

                # Valida o produto e o estoque
                produto = supermarket.fetch_one("SELECT value, quantity FROM Product WHERE id = %s", (product_id,))
                if not produto:
                    print("--> Produto não encontrado.")
                    continue
                
                estoque_disponivel = produto[1]
                preco_unitario = produto[0]

                quantidade = int(input(f"Digite a quantidade (disponível: {estoque_disponivel}): "))
                if quantidade <= 0 or quantidade > estoque_disponivel:
                    print("--> Quantidade inválida ou fora de estoque.")
                    continue

                # Adiciona ao carrinho
                carrinho.append({'id': product_id, 'qtd': quantidade, 'valor': preco_unitario})
                total_compra += quantidade * preco_unitario
                print(f"--> Produto adicionado! Total parcial: R${total_compra:.2f}")

            except ValueError:
                print("--> Por favor, digite um número válido.")

        if not carrinho:
            print("Nenhum produto no carrinho. Compra cancelada.")
            return

        # Início da Transação
        try:

            print(f"\nFinalizando compra. Total: R${total_compra:.2f}")

            payment_method = input("Write your payment method: ")

            # 1. Inserir o "cabeçalho" na tabela Sales e obter o ID da nova venda
            query_sales = sql.SQL("INSERT INTO Sales (client_id, payment_method, total_value) VALUES (%s, %s, %s) RETURNING id;")
            # RETURNING id é um recurso do PostgreSQL para obter o ID recém-criado
            data_to_send = (client_id, payment_method, total_compra)

            sale_id = supermarket.fetch_one(query_sales, data_to_send)[0]

            # 2. Loop no carrinho para inserir os itens e atualizar o estoque
            for item in carrinho:
                # 2a. Inserir em Sale_Items
                query_items = sql.SQL("INSERT INTO Sale_Items (sale_id, product_id, quantity, item_value) VALUES (%s, %s, %s, %s);")
                supermarket.execute_command(query_items, (sale_id, item['id'], item['qtd'], item['valor']))

                # 2b. Atualizar o estoque em Product
                query_stock = sql.SQL("UPDATE Product SET quantity = quantity - %s WHERE id = %s;")
                supermarket.execute_command(query_stock, (item['qtd'], item['id']))
            
            # 3. Se tudo deu certo, efetiva a transação
            print("\n--- Compra realizada com sucesso! ---")

        except Exception as e:
            # 4. Se algo deu errado, desfaz tudo
            print(f"\n--> Ocorreu um erro. A compra foi cancelada. Detalhe: {e}")

    else:
        print("O login deu errado!")

   

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