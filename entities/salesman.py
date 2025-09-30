class Salesman:
    def __init__(self):
        self.name = None
        self.password = None
        self.number = None
    
    def set_name(self, name):
        self.name = name

    def set_number(self, number):
        self.number = number

    def set_password(self, password):
        self.password = password

    @property
    def salesman(self):
        return self.name, self.password, self.number