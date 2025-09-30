from entities.purchase import Purchase

class Client:
    def __init__(self):
        self.name = None
        self.password = None
        self.phone = None
        self.purchases = []

    def set_name(self, name):
        self.name = name

    def set_password(self, password):
        self.password = password
    
    def set_phone(self, phone):
        self.phone = phone

    def check_password(self, attempt):
        if self.password == attempt:
            print("\n--> Correct Password!")
            return True
        
        else:
            print("\n--> Wrong Password!")
            return False

    def append_purchases(self, Purchase):
        purchases = Purchase.get_items 
        for i in purchases:
            self.purchases.append(i)

    @property
    def client(self):
        return self.name, self.password, self.phone, self.purchases