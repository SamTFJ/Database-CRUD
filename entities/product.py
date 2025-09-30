from backend.supermarket import Supermarket
from psycopg2 import sql

class Product:
    def __init__(self):
        self.name = None
        self.category = None
        self.quantity = None
        self.price = None
    
    def set_name(self, name):
        self.name = name

    def set_category(self, category):
        self.category = category

    def set_quantity(self, quantity):
        self.quantity = quantity

    def set_price(self, price):
        self.price = price

    @property
    def product(self):
        return self.name, self.category, self.quantity, self.price