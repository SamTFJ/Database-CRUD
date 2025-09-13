# manager.py
from dbconnection import DBconnect
from models import Produto
from typing import List, Optional, Tuple

class GerenciadorProduto:
    def __init__(self, db: Optional[DBconnect] = None):
        self.db = db or DBconnect()

    def insert(self, produto: Produto) -> int:
        produto.validate()
        query = """
            INSERT INTO item (name, value, quantity, category)
            VALUES (%s, %s, %s, %s)
            RETURNING id, created_at;
        """
        params = (produto.name.strip(), float(produto.value), int(produto.quantity), produto.category)
        result = self.db.execute_command(query, params, fetch=True)
        if result and result[0]:
            new_id, created_at = result[0][0], result[0][1]
            produto.id = new_id
            produto.created_at = created_at
            return new_id
        return -1

    def update_by_name(self, name: str, new_produto: Produto) -> int:
        # atualiza por name (atenção: nomes duplicados atualização em massa)
        new_produto.validate()
        query = """
            UPDATE item SET name = %s, value = %s, quantity = %s, category = %s
            WHERE name = %s
            RETURNING id;
        """
        params = (new_produto.name.strip(), float(new_produto.value), int(new_produto.quantity), new_produto.category, name)
        result = self.db.execute_command(query, params, fetch=True)
        return len(result) if result else 0

    def delete_by_name(self, name: str) -> int:
        query = "DELETE FROM item WHERE name = %s RETURNING id;"
        result = self.db.execute_command(query, (name,), fetch=True)
        return len(result) if result else 0

    def get_by_name(self, name: str) -> List[Produto]:
        query = "SELECT id, name, value, quantity, category, created_at FROM item WHERE name = %s;"
        rows = self.db.execute_command(query, (name,), fetch=True)
        produtos = []
        if rows:
            for row in rows:
                p = Produto(id=row[0], name=row[1], value=float(row[2]), quantity=int(row[3]), category=row[4], created_at=row[5])
                produtos.append(p)
        return produtos

    def list_all(self) -> List[Produto]:
        query = "SELECT id, name, value, quantity, category, created_at FROM item ORDER BY id;"
        rows = self.db.execute_command(query, fetch=True)
        produtos = []
        if rows:
            for row in rows:
                produtos.append(Produto(id=row[0], name=row[1], value=float(row[2]), quantity=int(row[3]), category=row[4], created_at=row[5]))
        return produtos

    def count(self) -> int:
        query = "SELECT COUNT(*) FROM item;"
        rows = self.db.execute_command(query, fetch=True)
        return int(rows[0][0]) if rows else 0

    def total_value(self) -> float:
        query = "SELECT COALESCE(SUM(value * quantity), 0) FROM item;"
        rows = self.db.execute_command(query, fetch=True)
        return float(rows[0][0]) if rows and rows[0][0] is not None else 0.0

    def report_by_category(self) -> List[Tuple[str, int, float, int]]:
        """
        Retorna lista de tuplas: (category, count_items, total_value_sum, total_quantity)
        """
        query = """
            SELECT
              COALESCE(category, 'Without category') as category,
              COUNT(*) as qty_items,
              COALESCE(SUM(value * quantity), 0) as total_value,
              COALESCE(SUM(quantity), 0) as total_quantity
            FROM item
            GROUP BY category
            ORDER BY category;
        """
        rows = self.db.execute_command(query, fetch=True)
        result = []
        if rows:
            for r in rows:
                result.append((r[0], int(r[1]), float(r[2]), int(r[3])))
        return result
