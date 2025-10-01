import entities.client as Client
import entities.salesman as Salesman
import entities.product as Product
import entities.sales as Sales
import entities.sale_items as SaleItems

# --- Menu para Funcionários (Salesman) ---
def main_salesman_menu():
    while True:
        print(f"{'-'*42}\n"
        f"{'-'*14} SALESMAN MENU {'-'*15}\n"
        f"{'-'*42}\n"
        '(1) Manage Products\n'
        '(2) Manage Clients\n'
        '(3) Manage Sales\n'
        '(4) Manage Salesmen\n'
        '(5) Generate Reports\n'
        '(0) Logout\n')

        try:
            option = int(input('Select an option: '))
            
            # Delega a tarefa para a função de menu do especialista apropriado.
            if option == 1:
                Product.product_crud_menu()
            elif option == 2:
                Client.clients_crud_menu()
            elif option == 3:
                Sales.sales_crud_menu()
            elif option == 4:
                Salesman.salesman_crud_menu()
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
        print(f"{'-'*42}\n"
        f"{'-'*16} CLIENT MENU {'-'*15}\n"
        f"{'-'*42}\n"
        '(1) View Products\n'
        '(2) Make a Purchase\n'
        '(3) View my Purchases\n'
        '(4) View my Data\n'
        '(8) Register as a new Client\n'
        '(9) Login\n'
        '(0) Back\n')

        try:
            option = int(input('Select an option: '))

            if option == 1:
                Product.list_items_product()
            elif option == 2:
                if Client.login_client():
                    Client.make_purchase()
            elif option == 3:
                if Client.login_client():
                    Client.view_my_purchases()
            elif option == 4:
                Client.view_my_data()
            elif option == 8:
                Client.insert_client()
            elif option == 0:
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
        print(f"{'-'*42}\n"
        f"{'-'*18} MAIN MENU {'-'*18}\n"
        f"{'-'*42}\n"
        '(1) Access as Salesman\n'
        '(2) Access as Client\n'
        '(0) Exit\n')

        try:
            option = int(input('Select an option: '))
            
            if option == 1:
                option2 = int(input('Register (1) or log in (2)?: '))
                if option2 == 2:
                    if Salesman.login_salesman():
                        main_salesman_menu() # Só então o menu principal do funcionário é chamado.
                    else:
                        print("Wrong credentials!")
                        main()
                else:
                    Salesman.insert_salesman()

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
    main()