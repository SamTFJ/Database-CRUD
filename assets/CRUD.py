from dbconnection import DBconnect
from psycopg2 import sql

class CRUD:
    def __init__ (self):
        self.db = DBconnect()

    def run(self):
        while True:
            print("             MENU")
            print("|=================================|")
            print("|     1 - Insert new item         |")
            print("|     2 - Update item             |")
            print("|     3 - Delete item             |")
            print("|     4 - Search for item         |")
            print("|     5 - Show all items          |")
            print("|     6 - Save and exit           |")
            print("|=================================|")

            choice = input("Select an option: ")

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
                self.EndConnection()
                print("Exiting application...")
                break
            else:
                print("Invalid option. Please try again.")

            if choice != '6':
                input("Press Enter to continue...")

    def insert_item(self):
        name = input("Write the name of the product: ")
        value = float(input("Write the value of the product (EX: 20.5): "))

        query = sql.SQL("INSERT INTO item (name, value) VALUES (%s, %s)")

        data_to_send = (name, value)

        self.db.execute_command(query, data_to_send)
        print("Item inserted")

    def update_item(self):
        name = input("Write the name of the product that will be updated: ")

        new_name = input("Write the new name of the product: ")
        new_value = input("Write the new value of the product: ")

        data_to_send = (new_name, new_value, name)

        query = sql.SQL("UPDATE item SET name = %s, value = %s WHERE name = %s;")

        self.db.execute_command(query, data_to_send)
        print("Item updated")

    def delete_item(self):
        name = input("Write the name of the product that will be deleted: ")

        data_to_send = (name,)

        query = sql.SQL("DELETE FROM item WHERE name = %s;")

        self.db.execute_command(query, data_to_send)
        print("Item deleted")
    
    def search_item(self):
        name = input("Write the name of the product to be searched: ")

        data_to_send = (name,)

        query = sql.SQL("SELECT * FROM item WHERE name = %s;")

        self.db.execute_command(query, data_to_send)

        result = self.db.cur.fetchall()

        if result:
            for i in result:
                print(i)
            print("Item found")
        else:
            print("Item not found")

    def list_collection(self):
        query1 = sql.SQL("SELECT COUNT(*) FROM item;")

        query2 = sql.SQL("SELECT SUM(value) FROM item;")

        query3 = sql.SQL("SELECT * FROM item;")

        self.db.execute_command(query1)

        result1 = self.db.cur.fetchall()

        print("The quantity of items stored is: ",result1[0][0])
        
        self.db.execute_command(query2)

        result2 = self.db.cur.fetchall()

        print("The total sum of values in items is: ", result2[0][0])

        self.db.execute_command(query3)

        result3 = self.db.cur.fetchall()

        if result3:
            for i in result3:
                print(i)
            print("Items found")
        else:
            print("Items not found")

    def EndConnection(self):
        self.db.end_connection()
        print("Connection with the database endend")

if __name__ == "__main__":
    crud = CRUD()
    crud.run()