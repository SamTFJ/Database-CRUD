from backend.supermarket import Supermarket
from psycopg2 import sql

class SaleItems:
    def __init__(self):
        self.id = None
        self.name = None
        self.password = None
        self.number = None
    
    def set_name(self, name):
        self.name = name

    def set_id(self, id):
        self.id = id

    def set_password(self, password):
        self.password = password

    def check_password(self, attempt):
        if self.password == attempt:
            print("\n--> Correct Password!")
            return True
        
        else:
            print("\n--> Wrong Password!")
            return False

    def set_password(self, password):
        self.password = password

    @property
    def sale_items(self):
        return self.id, self.name, self.password, self.number