from backend.supermarket import Supermarket
from psycopg2 import sql
supermarket = Supermarket()

def coletar_dados_produto():
    """Função auxiliar para coletar e validar os dados de um produto."""
    name = input("\n--> Write the name of the product: ").strip()
    # Adiciona a validação do seu amigo para garantir que o nome não seja vazio
    while not name:
        print("\n--> Name is required!")
        name = input("--> Write the name of the product: ").strip()

    value = float(input("--> Write the value of the product (EX: 20.5): "))
    category = input("--> Write the category of the product: ").strip()
    quantity = int(input("--> Write the quantity in stock: "))
    return (name, value, category, quantity)

def insert_item_product():
    """Cadastra um novo produto no banco de dados."""
    print("\n--- Register New Product ---")
    # Usa a função auxiliar para pegar os dados
    dados = coletar_dados_produto()
    
    # Prepara a query com todas as colunas necessárias
    query = sql.SQL("INSERT INTO Product (name, value, category, quantity) VALUES (%s, %s, %s, %s)")
    
    if supermarket.execute_command(query, dados):
        print(f"\n--> Product '{dados[0]}' registered successfully!")
    
    input("\n--> Press Enter to continue...")

def update_item_product():
    """Altera os dados de um produto existente."""
    print("\n--- Update Product ---")
    product_id = int(input("--> Enter the ID of the product to update: ").strip())
    
    # Busca o produto para garantir que ele existe
    product = supermarket.fetch_one(sql.SQL("SELECT * FROM Product WHERE id = %s"), (product_id,))
    
    if not product:
        print(f"\n--> Product with ID {product_id} not found.")
        input("\n--> Press Enter to continue...")
        return

    print("\n--> Product Found. Enter the new data:")
    # Usa a função auxiliar para coletar os novos dados
    novos_dados = coletar_dados_produto()
    
    # Prepara a query de UPDATE
    query = sql.SQL("UPDATE Product SET name = %s, value = %s, category = %s, quantity = %s, last_update = CURRENT_TIMESTAMP WHERE id = %s")
    # Junta os novos dados com o ID do produto
    dados_para_enviar = (*novos_dados, product_id)

    if supermarket.execute_command(query, dados_para_enviar):
        print(f"\n--> Product ID {product_id} updated successfully!")
    
    input("\n--> Press Enter to continue...")

def list_items_product():
    """Lista todos os produtos cadastrados."""
    print("\n--- Listing All Products ---")
    query = sql.SQL("SELECT id, name, value, quantity FROM Product ORDER BY name")
    products = supermarket.fetch_all(query)

    if products:
        # Imprime de forma simples, como no seu código original
        for product in products:
            print(product)
        print("\n--> Items found")
    else:
        print("\n--> No products found.")
    
    input("\n--> Press Enter to continue...")

def search_by_id_product():
    """Busca e exibe um produto específico pelo seu ID."""
    print("\n--- Search Product by ID ---")
    product_id = int(input("--> Write the ID of the product to be searched: ").strip())
    
    query = sql.SQL("SELECT * FROM Product WHERE id = %s")
    product = supermarket.fetch_one(query, (product_id,))

    if product:
        # Imprime o resultado bruto
        print(product)
        print("\n--> Item found")
    else:
        print(f"\n--> Product with ID {product_id} not found.")
    
    input("\n--> Press Enter to continue...")

def search_by_name_product():
    """Busca produtos por parte do nome."""
    print("\n--- Search Product by Name ---")
    name = input("--> Write the name (or part of it) of the product: ").strip()
    
    query = sql.SQL("SELECT id, name, value, quantity FROM Product WHERE name ILIKE %s ORDER BY name")
    products = supermarket.fetch_all(query, (f"%{name}%",))

    if products:
        for product in products:
            print(product)
        print(f"\n--> Found {len(products)} item(s).")
    else:
        print(f"\n--> No products found with the name '{name}'.")
    
    input("\n--> Press Enter to continue...")

def delete_item_product():
    """Remove um produto do banco de dados pelo seu ID."""
    print("\n--- Delete Product ---")
    product_id = int(input("--> Write the ID of the product that will be deleted: ").strip())
    
    # Adiciona a confirmação, que é uma boa prática simples
    confirmation = input(f"--> Are you sure you want to delete product ID {product_id}? (s/n): ").strip().lower()
    
    if confirmation == 's':
        query = sql.SQL("DELETE FROM Product WHERE id = %s")
        if supermarket.execute_command(query, (product_id,)):
            print("\n--> Product deleted successfully.")
    else:
        print("\n--> Operation cancelled.")
        
    input("\n--> Press Enter to continue...")

def filter_products_advanced(is_employee=False):
    """Filtro avançado para produtos, conforme especificação do professor."""
    print("\n--- Advanced Product Filter ---")
    # Monta a query base
    query_str = "SELECT id, name, value, quantity FROM Product WHERE 1=1"
    params = []
    
    # Coleta os filtros
    name = input("--> Filter by name (leave blank for all): ").strip()
    price_min_str = input("--> Filter by minimum price (leave blank for all): ").strip()
    price_max_str = input("--> Filter by maximum price (leave blank for all): ").strip()
    category = input("--> Filter by category (leave blank for all): ").strip()
    
    # Lógica para o funcionário (requisito do professor)
    if is_employee:
        low_stock_filter = input("--> Filter by low stock (< 5 units)? (s/n): ").strip().lower()
        if low_stock_filter == 's':
            query_str += " AND quantity < %s"
            params.append(5)

    # Adiciona os filtros à query dinamicamente
    if name:
        query_str += " AND name ILIKE %s"
        params.append(f"%{name}%")
    if price_min_str:
        query_str += " AND value >= %s"
        params.append(float(price_min_str))
    if price_max_str:
        query_str += " AND value <= %s"
        params.append(float(price_max_str))
    if category:
        query_str += " AND category ILIKE %s"
        params.append(f"%{category}%")

    # Executa a busca
    products = supermarket.fetch_all(sql.SQL(query_str), params)

    if products:
        for product in products:
            print(product)
        print(f"\n--> Found {len(products)} item(s) with the specified filters.")
    else:
        print("\n--> No products found with the specified filters.")
            
    input("\n--> Press Enter to continue...")

def product_crud_menu():

    print(f'{'-'*42}\n'
    f'{'-'*18} MENU {'-'*18}\n'
    f'{'-'*42}\n'
    '(1) Register Product\n'
    '(2) Update Product\n'
    '(3) List All Products\n'
    '(4) Search by ID\n'
    '(5) Search by Name\n'
    '(6) Delete Product\n'
    '(7) Advanced Filter\n'
    '(0) Back)')

    try:
        option = int(input('Opção: '))
        if option == 1:
            insert_item_product()
        elif option == 2:
            update_item_product()
        elif option == 3:
            list_items_product()
        elif option == 4:
            search_by_id_product()
        elif option == 5:
            search_by_name_product()
        elif option == 6:
            delete_item_product()
        elif option == 7:
            filter_products_advanced(is_employee=is_employee)
        elif option == 0:
            return
        else:
            print("\n--> Invalid Option!")
            input("\n--> Press Enter...")
            product_crud_menu()
    except Exception as e:
        print(f"Erro: {e}")
        input("\n--> Press Enter...")
        product_crud_menu()