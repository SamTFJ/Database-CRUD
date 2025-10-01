from backend.supermarket import Supermarket
from psycopg2 import sql
supermarket = Supermarket()

# --- FUNÇÕES DO "MINI-CRUD" DE VENDAS ---

def register_sale():
    print("\n--- Register New Sale---")
    # ETAPA 1: Coletar e validar ID do cliente e do vendedor.
    # ETAPA 2: Criar um loop para adicionar produtos ao "carrinho", validando estoque.
    # ETAPA 3: Calcular o valor total da venda.
    # ETAPA 4: Inserir o "cabeçalho" da venda na tabela 'Sales' e obter o novo 'sale_id'.
    # ETAPA 5: Inserir cada item do carrinho na tabela 'Sale_Items'.
    # ETAPA 6: Atualizar o estoque dos produtos na tabela 'Product'.
    print("Função de cadastro ainda não implementada.")
    input("\n--> Press Enter to continue...")


def list_sales():
    print("\n--- Listing All Sales ---")
    try:
        # Query com JOIN para buscar os nomes em outras tabelas
        query = sql.SQL("""
            SELECT s.id, c.name AS client_name, sm.name AS salesman_name, s.total_value, s.sale_date
            FROM Sales s
            JOIN Client c ON s.client_id = c.id
            JOIN Salesman sm ON s.salesman_id = sm.id
            ORDER BY s.sale_date DESC
        """)
        
        sales = supermarket.fetch_all(query)

        if not sales:
            print("--> No sales found.")
            return

        print("-" * 120)
        # Formata a saída para o usuário
        for sale in sales:
            print(
                f"ID: {sale['id']:<5} | "
                f"Data: {sale['sale_date'].strftime('%d/%m/%Y'):<12} | "
                f"Client: {sale['client_name']:<25} | "
                f"Salesman: {sale['salesman_name']:<25} | "
                f"Total: R$ {sale['total_value']:.2f}"
            )
        print("-" * 120)

    except Exception as e:
        print(f"\n--> An error occurred while listing sales: {e}")
    finally:
        input("\n--> Press Enter to continue...")


def search_sale_by_id():
    print("\n--- Search Sale by ID ---")
    try:
        sale_id = int(input("Digite o ID da venda: ").strip())

        query = sql.SQL("""
            SELECT s.id, c.name AS client_name, sm.name AS salesman_name, s.total_value, s.sale_date
            FROM Sales s
            JOIN Client c ON s.client_id = c.id
            JOIN Salesman sm ON s.salesman_id = sm.id
            WHERE s.id = %s
        """)
        
        venda = supermarket.fetch_one(query, (sale_id,))

        if venda:
            print("\n--- Sale Found ---")
            print(f"Sale ID:   {venda['id']}")
            print(f"Data:          {venda['sale_date'].strftime('%d/%m/%Y %H:%M')}")
            print(f"Client:       {venda['client_name']}")
            print(f"Salesman:      {venda['salesman_name']}")
            print(f"Total Value:   R$ {venda['total_value']:.2f}")
            # Você poderia adicionar aqui uma busca na tabela Sale_Items para mostrar os produtos
        else:
            print(f"\n--> No sales found with ID {sale_id}.")

    except ValueError:
        print("\n--> Error: Invalid ID. Please enter a number.")
    except Exception as e:
        print(f"\n--> An unexpected error occurred: {e}")
    finally:
        input("\n--> Press Enter to continue...")

# --- MENU DE INTERFACE COM O USUÁRIO ---

def sales_crud_menu():
    # O loop while True pode ser colocado aqui ou no main.py, como fez o seu amigo.
    # Colocar no main.py é um pouco mais organizado.
    print(f"""{'-'*42}
{'-'*18} MENU VENDAS {'-'*18}
{'-'*42}
(1) Cadastrar Nova Venda
(2) Listar Todas as Vendas
(3) Buscar Venda por ID
(4) Buscar Vendas por Cliente (a fazer)
(5) Deletar Venda (a fazer)
(0) Voltar""")

    try:
        option = int(input('Opção: '))
        if option == 1: register_sale()
        elif option == 2: list_sales()
        elif option == 3: search_sale_by_id()
        # elif option == 4: ...
        # elif option == 5: ...
        elif option == 0:
            return
        else:
            print("\n--> Opção Inválida!")
    except (ValueError, TypeError):
        print("\n--> Por favor, digite um número válido.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        input("\n--> Pressione Enter para retornar ao menu...")
        sales_crud_menu()