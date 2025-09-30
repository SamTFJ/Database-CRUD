from backend.supermarket import Supermarket
from psycopg2 import sql

class Purchase:
    def __init__(self):
        # Será preenchido com Tuplas (Produto, Quantidade)
        self.items = []
        self.paymethod = None

    def set_items(self, item):
        self.items.append(item)

    def set_paymethod(self, paymethod):
        self.paymethod = paymethod

    # Decorator que permite que um atributo possa ser acessado como se fosse uma variável simples
    # Ou seja em vez de usar purchase.get_items() se usa purchase.get_item, sem o parênteses
    @property
    def get_items(self):
        return self.items