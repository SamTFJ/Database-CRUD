class Salesman:
    def __init__(self):
        self.name = None
        self.id = None
        self.password = None
    
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

    @property
    def salesman(self):
        return self.name, self.id