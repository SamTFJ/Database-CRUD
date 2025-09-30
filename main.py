import entities.client as Client
import entities.salesman as Salesman
import entities.product as Product
import entities.sales as Sales
import entities.sale_items as SaleItems

# --- Menu para Funcionários (Salesman) ---
def main_salesman_menu():
    """Apresenta o menu de gerenciamento para funcionários logados."""
    while True:
        # Apresenta as opções de gerenciamento que um funcionário pode acessar.
        print(f"""{'-'*42}
{'-'*14} SALESMAN MENU {'-'*15}
{'-'*42}
(1) Manage Products
(2) Manage Clients
(3) Manage Sales
(4) Manage Salesmen
(5) Generate Reports
(0) Logout""")

        try:
            option = int(input('Select an option: '))
            
            # Delega a tarefa para a função de menu do especialista apropriado.
            if option == 1:
                Product.products_crud_menu()
            elif option == 2:
                Client.clients_crud_menu()
            elif option == 3:
                Sales.sales_crud_menu()
            elif option == 4:
                Salesman.salesmen_crud_menu()
            # elif option == 5:
                # Chame função de gerar relatórios.
                # report.reports_menu()
            elif option == 0:
                print("\nLogging out from salesman area...")
                break
            else:
                print("\n--> Invalid Option!")

        except (ValueError, TypeError):
            print("\n--> Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        input("\n--> Press Enter to continue...")


# --- Menu para Clientes (Client) ---
def main_client_menu():
    """Apresenta o menu de ações para clientes."""
    while True:
        # Apresenta as opções que um cliente pode realizar.
        print(f"""{'-'*42}
{'-'*16} CLIENT MENU {'-'*15}
{'-'*42}
(1) View Products
(2) Make a Purchase
(3) View my Purchases
(4) View my Data
(8) Register as a new Client
(9) Login
(0) Back""")

        try:
            option = int(input('Select an option: '))

            if option == 1:
                # Qualquer um pode ver os produtos, não precisa de login.
                Product.list_products_for_client()
            elif option == 2:
                # Ação que exige login.
                Client.make_purchase()
            elif option == 3:
                # Ação que exige login.
                Client.view_my_purchases()
            elif option == 4:
                # Ação que exige login.
                Client.view_my_data()
            elif option == 8:
                # Delega a tarefa de cadastro para o especialista em clientes.
                Client.register_client()
            elif option == 9:
                # Delega a tarefa de login para o especialista.
                Client.login_client()
            elif option == 0:
                # Encerra o loop e volta para o menu principal.
                break
            else:
                print("\n--> Invalid Option!")

        except (ValueError, TypeError):
            print("\n--> Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        input("\n--> Press Enter to continue...")


# --- Função Principal (A "Recepção") ---
def main():
    """Função principal que inicia o programa e direciona o usuário."""
    # O loop principal do programa. Continua até o usuário escolher sair.
    while True:
        # Mostra o primeiro menu, perguntando o tipo de usuário.
        print(f"""{'-'*42}
{'-'*15} MAIN MENU {'-'*16}
{'-'*42}
(1) Access as Salesman
(2) Access as Client
(0) Exit""")

        try:
            option = int(input('Select an option: '))
            
            if option == 1:
                # Antes de entrar no menu de funcionário, é preciso fazer login.
                # A função de login do vendedor deve retornar True se o login for bem-sucedido.
                if Salesman.login_salesman():
                    main_salesman_menu() # Só então o menu principal do funcionário é chamado.
            
            elif option == 2:
                # Delega para o menu de clientes.
                main_client_menu()

            elif option == 0:
                # Encerra o programa.
                print("\nExiting application...")
                Client.close_connection() # Assumindo que a função está no client_manager.
                break
            
            else:
                print('\n--> Invalid Option!')

        except (ValueError, TypeError):
            print("\n--> Invalid input. Please enter a number.")
        except Exception as e:
            print(f'An unexpected error occurred in the main menu: {e}')
        
        input('\n--> Press Enter to continue...')


# --- Ponto de Entrada do Programa ---
if __name__ == "__main__":
    # Esta linha inicia todo o programa, chamando a função principal.
    main()