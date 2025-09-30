from backend.supermarket import Supermarket
from psycopg2 import sql
supermarket = Supermarket()

class Sale:
    def __init__(self):
        # Inicializa todos os atributos que correspondem às colunas da tabela 'Sales'
        self.id = None
        self.client_id = None
        self.salesman_id = None
        self.payment_method = None
        self.total_value = None
        self.sale_date = None
    
    # Métodos 'set' para definir o valor de cada atributo
    def set_id(self, sale_id):
        self.id = sale_id

    def set_client_id(self, client_id):
        self.client_id = client_id
        
    def set_salesman_id(self, salesman_id):
        self.salesman_id = salesman_id

    def set_payment_method(self, payment_method):
        self.payment_method = payment_method
        
    def set_total_value(self, total_value):
        self.total_value = total_value
        
    def set_sale_date(self, sale_date):
        self.sale_date = sale_date

    # Propriedade para retornar todos os atributos da venda em uma tupla
    @property
    def sale(self):
        return (
            self.id,
            self.client_id,
            self.salesman_id,
            self.payment_method,
            self.total_value,
            self.sale_date
        )
    
def sales_crud_menu():
    print(f"""{'-'*42}
{'-'*18} MENU {'-'*18}
{'-'*42}
Cadastrar (1)
Listar (2)
Procurar por ID (3)
Procurar por cliente (4)
Deletar (5)
Voltar (0)""")

    try:
        option = int(input('Opção: '))
        if option == 1: None
        elif option == 2: None
        elif option == 3: None
        elif option == 4: None
        elif option == 5: None
        elif option == 0: return
        else:
            print("\n--> Invalid Option!")
            input("\n--> Press Enter...")
            sales_crud_menu()
    except Exception as e:
        print(f"Erro: {e}")
        input("\n--> Press Enter...")
        sales_crud_menu()