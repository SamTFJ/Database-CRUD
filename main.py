# main.py
from manager import GerenciadorProduto
from models import Produto

# --- Funções Auxiliares de Input ---

def prompt_int(prompt: str, default: int = 0) -> int:
    """
    Solicita ao usuário uma entrada numérica inteira de forma segura.
    Continua pedindo até que um número válido seja inserido.
    Se o usuário apenas pressionar Enter, retorna o valor padrão.
    """
    while True:
        try:
            val = input(prompt)
            # Se a entrada for vazia, usa o valor padrão
            if val.strip() == "":
                return default
            # Tenta converter a entrada para inteiro
            return int(val)
        except ValueError:
            # Informa o usuário em caso de erro de conversão
            print("Por favor, digite um número inteiro válido.")

def prompt_float(prompt: str, default: float = 0.0) -> float:
    """
    Solicita ao usuário uma entrada numérica de ponto flutuante (float) de forma segura.
    Continua pedindo até que um número válido seja inserido.
    Se o usuário apenas pressionar Enter, retorna o valor padrão.
    """
    while True:
        try:
            val = input(prompt)
            # Se a entrada for vazia, usa o valor padrão
            if val.strip() == "":
                return default
            # Tenta converter a entrada para float
            return float(val)
        except ValueError:
            # Informa o usuário em caso de erro de conversão
            print("Por favor, digite um número válido (ex: 12.50).")

# --- Classe Principal da Interface ---

class CRUD:
    """
    Classe que gerencia a interface de usuário (menu) e orquestra as operações
    de Inserir, Atualizar, Deletar e Consultar produtos.
    """
    def __init__(self):
        # Inicializa o gestor, que é a camada de lógica para interagir com o banco de dados
        self.gestor = GerenciadorProduto()

    def run(self):
        """
        Inicia o loop principal da aplicação, exibindo o menu e aguardando a escolha do usuário.
        """
        # O loop 'while True' mantém o menu ativo até que a opção de sair seja escolhida
        while True:
            # Exibição do menu principal
            print("\n -> HIPERMERCADO SPEED, BEM-VINDO!")
            print("\n               MENU")
            print("|=================================|")
            print("|     1 - Inserir novo item       |")
            print("|     2 - Atualizar item          |")
            print("|     3 - Deletar item            |")
            print("|     4 - Buscar por item         |")
            print("|     5 - Mostrar todos os itens  |")
            print("|     6 - Relatório de estoque    |")
            print("|     7 - Salvar e sair           |")
            print("|=================================|")

            choice = input("-> Selecione uma opção: ").strip()

            # O bloco try...except captura erros inesperados para evitar que o programa feche
            try:
                # Roteamento da escolha do usuário para o método correspondente
                if choice == '1':
                    self.insert_item()
                elif choice == '2':
                    self.update_item()
                elif choice == '3':
                    self.delete_item()
                elif choice == '4':
                    self.search_item()
                elif choice == '5':
                    self.list_collection()
                elif choice == '6':
                    self.report_by_category()
                elif choice == '7':
                    # Encerra a conexão e sai do loop
                    self.EndConnection()
                    print("\nSaindo da aplicação...")
                    break
                else:
                    print("\nOpção inválida. Por favor, tente novamente.")
            except Exception as e:
                print("\nOcorreu um erro inesperado:", e)

            # Pausa a execução para que o usuário possa ler a saída antes de o menu ser exibido novamente
            if choice != '7':
                input("\nPressione Enter para continuar...")

    def insert_item(self):
        """Coleta os dados do novo produto e solicita ao gestor para inseri-lo no banco."""
        print("\n--- INSERIR NOVO ITEM ---")
        name = input("-> Digite o nome do produto: ").strip()
        value = prompt_float("-> Digite o valor do produto (EX: 20.50): ")
        quantity = prompt_int("-> Digite a quantidade (EX: 10): ")
        category = input("-> Digite a categoria (opcional): ").strip() or None

        # Cria um objeto 'Produto' com os dados fornecidos
        prod = Produto(name=name, value=value, quantity=quantity, category=category)
        try:
            # Chama o método de inserção do gestor
            new_id = self.gestor.insert(prod)
            print(f"\nItem inserido com sucesso! ID: {new_id}")
        except Exception as e:
            print("\nFalha ao inserir o item:", e)

    def update_item(self):
        """Coleta os dados de um produto existente e solicita ao gestor para atualizá-lo."""
        print("\n--- ATUALIZAR ITEM ---")
        name = input("-> Digite o nome do produto que será atualizado: ").strip()
        
        print("\n-> Digite os novos valores (deixe em branco para cancelar):")
        new_name = input("-> Digite o novo nome do produto: ").strip()
        # Se o novo nome for vazio, cancela a operação
        if not new_name:
            print("\nAtualização cancelada (nome vazio).")
            return
            
        new_value = prompt_float("-> Digite o novo valor do produto: ")
        new_quantity = prompt_int("-> Digite a nova quantidade: ")
        new_category = input("-> Digite a nova categoria (opcional): ").strip() or None

        # Cria um objeto 'Produto' com os novos dados
        new_prod = Produto(name=new_name, value=new_value, quantity=new_quantity, category=new_category)
        try:
            # Chama o método de atualização do gestor
            updated = self.gestor.update_by_name(name, new_prod)
            print(f"\nRegistros atualizados: {updated}")
        except Exception as e:
            print("\nFalha ao atualizar:", e)

    def delete_item(self):
        """Solicita o nome de um produto e pede ao gestor para deletá-lo após confirmação."""
        print("\n--- DELETAR ITEM ---")
        name = input("-> Digite o nome do produto que será deletado: ").strip()
        # Pede confirmação para evitar exclusões acidentais
        confirm = input(f"\n-> Tem certeza que quer deletar todos os itens com o nome '{name}'? (s/N): ").lower()
        if confirm != 's':
            print("\nOperação cancelada.")
            return
        
        try:
            # Chama o método de deleção do gestor
            deleted = self.gestor.delete_by_name(name)
            print(f"\nRegistros deletados: {deleted}")
        except Exception as e:
            print("\nFalha ao deletar:", e)

    def search_item(self):
        """Busca por um produto pelo nome e exibe os resultados encontrados."""
        print("\n--- BUSCAR ITEM ---")
        name = input("-> Digite o nome do produto a ser buscado: ").strip()
        try:
            # Chama o método de busca do gestor
            results = self.gestor.get_by_name(name)
            if results:
                print("\n--- RESULTADOS ENCONTRADOS ---")
                for p in results:
                    print(f"ID: {p.id} | Nome: {p.name} | Valor: R${p.value:.2f} | Qtd: {p.quantity} | Categoria: {p.category} | Data: {p.created_at}")
            else:
                print("\nNenhum item encontrado com este nome.")
        except Exception as e:
            print("\nOcorreu um erro durante a busca:", e)

    def list_collection(self):
        """Lista todos os produtos cadastrados no banco de dados e exibe um resumo."""
        print("\n--- LISTA DE TODOS OS ITENS ---")
        try:
            # Obtém dados de resumo do gestor
            qtd = self.gestor.count()
            total = self.gestor.total_value()
            print("\nQuantidade total de itens cadastrados:", qtd)
            print(f"Valor total do inventário: R$ {total:.2f}\n")
            
            # Obtém a lista de todos os produtos
            produtos = self.gestor.list_all()
            if produtos:
                for p in produtos:
                    print(f"ID: {p.id} | Nome: {p.name} | Valor: R${p.value:.2f} | Qtd: {p.quantity} | Categoria: {p.category} | Data: {p.created_at}")
                    print("-" * 130)
            else:
                print("\nNão há itens cadastrados.")
        except Exception as e:
            print("\nOcorreu um erro ao listar a coleção:", e)

    def report_by_category(self):
        """Gera e exibe um relatório que agrupa os produtos por categoria."""
        print("\n--- RELATÓRIO DE ESTOQUE POR CATEGORIA ---")
        try:
            # Solicita o relatório ao gestor
            report = self.gestor.report_by_category()
            if not report:
                print("\nNão há dados para gerar o relatório.")
                return
            
            # Formata e exibe o cabeçalho da tabela
            print("\n{:<30} {:>8} {:>15} {:>10}".format("Categoria", "Itens", "Valor Total", "Quantidade"))
            print("-" * 70)
            # Itera sobre os dados do relatório e exibe cada linha formatada
            for cat, qty_items, total_value, total_quantity in report:
                print("{:<30} {:>8} {:>15.2f} {:>10}".format(cat, qty_items, total_value, total_quantity))
        except Exception as e:
            print("\nOcorreu um erro ao gerar o relatório:", e)

    def EndConnection(self):
        """Encerra a conexão com o banco de dados de forma segura."""
        try:
            # Chama o método de encerramento da conexão através do gestor
            self.gestor.db.end_connection()
            print("\nConexão com o banco de dados encerrada com sucesso.")
        except Exception as e:
            print("\nOcorreu um erro ao encerrar a conexão:", e)

# --- Ponto de Entrada da Aplicação ---

# O bloco 'if __name__ == "__main__"' garante que o código abaixo só será executado
# quando este arquivo (main.py) for rodado diretamente.
if __name__ == "__main__":
    # Cria uma instância da classe CRUD
    crud = CRUD()
    # Inicia a aplicação
    crud.run()