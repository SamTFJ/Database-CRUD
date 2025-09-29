class Salesman:
    def __init__(self):
        self.name = None
        self.number = None
    
    def set_name(self, name):
        self.name = name

    def set_number(self, number):
        self.number = number

    @property
    def salesman(self):
        return self.name, self.number