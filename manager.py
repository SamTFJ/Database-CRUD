# manager.py
from db_connection import DBconnect
from models import Produto
from typing import List, Optional, Tuple

class GerenciadorProduto:
    """
    Esta classe é a camada de lógica de negócios.
    Ela faz a ponte entre a interface do usuário (main.py) e a conexão com o banco de dados (db_connection.py).
    Todas as queries SQL e a manipulação de dados dos produtos estão centralizadas aqui.
    """
    def __init__(self, db: Optional[DBconnect] = None):
        # Permite injetar uma conexão de banco de dados (útil para testes)
        # ou cria uma nova conexão por padrão se nenhuma for fornecida.
        self.db = db or DBconnect()

    def insert(self, produto: Produto) -> int:
        """
        Insere um novo produto no banco de dados.
        - Valida os dados do produto antes de inserir.
        - Retorna o ID do produto recém-criado.
        """
        # Garante que os dados do produto (nome, valor, etc.) são válidos antes de prosseguir.
        produto.validate()
        
        # A cláusula 'RETURNING id, created_at' do PostgreSQL é uma otimização:
        # ela insere e retorna os valores gerados (como o ID serial) em uma única operação.
        query = """
            INSERT INTO item (name, value, quantity, category)
            VALUES (%s, %s, %s, %s)
            RETURNING id, created_at;
        """
        # Os parâmetros são passados como uma tupla para o método de execução,
        # o que protege a aplicação contra ataques de SQL Injection.
        params = (produto.name.strip(), float(produto.value), int(produto.quantity), produto.category)
        result = self.db.execute_command(query, params, fetch=True)
        
        # Se a inserção foi bem-sucedida, atualiza o objeto 'produto' com o ID e data de criação.
        if result and result[0]:
            new_id, created_at = result[0][0], result[0][1]
            produto.id = new_id
            produto.created_at = created_at
            return new_id
        # Retorna -1 para indicar que a inserção falhou.
        return -1

    def update_by_name(self, name: str, new_produto: Produto) -> int:
        """
        Atualiza um ou mais produtos com base no nome.
        ATENÇÃO: Se houver produtos com nomes duplicados, todos serão atualizados.
        - Retorna a quantidade de registros que foram atualizados.
        """
        new_produto.validate()
        query = """
            UPDATE item SET name = %s, value = %s, quantity = %s, category = %s
            WHERE name = %s
            RETURNING id;
        """
        params = (new_produto.name.strip(), float(new_produto.value), int(new_produto.quantity), new_produto.category, name)
        result = self.db.execute_command(query, params, fetch=True)
        # Retorna o número de linhas afetadas pela atualização.
        return len(result) if result else 0

    def delete_by_name(self, name: str) -> int:
        """
        Deleta um ou mais produtos com base no nome.
        - Retorna a quantidade de registros que foram deletados.
        """
        query = "DELETE FROM item WHERE name = %s RETURNING id;"
        result = self.db.execute_command(query, (name,), fetch=True)
        # Retorna o número de linhas afetadas pela deleção.
        return len(result) if result else 0

    def get_by_name(self, name: str) -> List[Produto]:
        """
        Busca todos os produtos que correspondem a um determinado nome.
        - Retorna uma lista de objetos 'Produto'.
        """
        query = "SELECT id, name, value, quantity, category, created_at FROM item WHERE name = %s;"
        rows = self.db.execute_command(query, (name,), fetch=True)
        produtos = []
        if rows:
            # Transforma cada linha (tupla) retornada do banco de dados em um objeto 'Produto'.
            for row in rows:
                p = Produto(id=row[0], name=row[1], value=float(row[2]), quantity=int(row[3]), category=row[4], created_at=row[5])
                produtos.append(p)
        return produtos

    def list_all(self) -> List[Produto]:
        """
        Lista todos os produtos cadastrados, ordenados pelo ID.
        - Retorna uma lista de objetos 'Produto'.
        """
        query = "SELECT id, name, value, quantity, category, created_at FROM item ORDER BY id;"
        rows = self.db.execute_command(query, fetch=True)
        produtos = []
        if rows:
            # Assim como em 'get_by_name', transforma os resultados brutos em objetos.
            for row in rows:
                produtos.append(Produto(id=row[0], name=row[1], value=float(row[2]), quantity=int(row[3]), category=row[4], created_at=row[5]))
        return produtos

    def count(self) -> int:
        """Conta o número total de itens na tabela."""
        query = "SELECT COUNT(*) FROM item;"
        rows = self.db.execute_command(query, fetch=True)
        # O resultado de COUNT(*) é sempre uma linha com uma coluna.
        return int(rows[0][0]) if rows else 0

    def total_value(self) -> float:
        """Calcula o valor total do inventário (soma de valor * quantidade)."""
        # A função COALESCE(SUM(...), 0) garante que, se a tabela estiver vazia
        # e o SUM retornar NULL, o resultado final seja 0 em vez de None.
        query = "SELECT COALESCE(SUM(value * quantity), 0) FROM item;"
        rows = self.db.execute_command(query, fetch=True)
        return float(rows[0][0]) if rows and rows[0][0] is not None else 0.0

    def report_by_category(self) -> List[Tuple[str, int, float, int]]:
        """
        Gera um relatório que agrupa os produtos por categoria, calculando totais.
        Retorna uma lista de tuplas, onde cada tupla contém:
        (nome_da_categoria, contagem_de_itens, soma_do_valor_total, soma_da_quantidade_total)
        """
        query = """
            SELECT
                -- Se a categoria for nula, exibe como 'Sem categoria'
                COALESCE(category, 'Sem categoria') as category,
                -- Conta quantos produtos existem em cada grupo (categoria)
                COUNT(*) as qty_items,
                -- Soma o valor total (valor * quantidade) para cada categoria
                COALESCE(SUM(value * quantity), 0) as total_value,
                -- Soma a quantidade total de itens para cada categoria
                COALESCE(SUM(quantity), 0) as total_quantity
            FROM item
            -- Agrupa todas as linhas pela coluna 'category' para que as funções de agregação (COUNT, SUM) funcionem
            GROUP BY category
            -- Ordena o resultado final pelo nome da categoria
            ORDER BY category;
        """
        rows = self.db.execute_command(query, fetch=True)
        result = []
        if rows:
            # Converte os resultados brutos para os tipos Python corretos (int, float).
            for r in rows:
                result.append((r[0], int(r[1]), float(r[2]), int(r[3])))
        return result