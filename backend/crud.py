from backend.supermarket import Supermarket
from psycopg2 import sql

class CRUD:
    def __init__ (self, type):
        self.supermarket = Supermarket()
        self.type = type
        
    def run(self):
        while True:
            print("             MENU")
            print("|=================================|")
            print("|     1 - Insert new item         |")
            print("|     1 - Insert new item         |")
            print("|     1 - Insert new item         |")
            print("|     2 - Update item             |")
            print("|     3 - Delete item             |")
            print("|     4 - Search for item         |")
            print("|     6 - Generate Stock Report   |")
            print("|     7 - Save and exit           |")
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
                self.generate_stock_report()
            elif choice == '7':
                self.EndConnection()
                print("Exiting application...")
                break
            else:
                print("Invalid option. Please try again.")

            if choice != '7':
                input("\nPress Enter to continue...")

    def insert_item(self):
        name = input("Write the name of the product: ")
        value = float(input("Write the value of the product (EX: 20.5): "))
        quantity = int(input("Write the quantity in stock: "))

        query = sql.SQL("INSERT INTO item (name, value, quantity) VALUES (%s, %s, %s)")

        data_to_send = (name, value, quantity)

        self.supermarket.execute_command(query, data_to_send)
        print("Item inserted")

    def update_item(self):
        name = input("Write the name of the product that will be updated: ")

        new_name = input("Write the new name of the product: ")
        new_value = input("Write the new value of the product: ")
        new_quantity = int(input("Write the new quantity: "))

        data_to_send = (new_name, new_value, new_quantity, 'now()', name)

        query = sql.SQL("UPDATE item SET name = %s, value = %s, quantity = %s, last_update = %s WHERE name = %s;")

        self.supermarket.execute_command(query, data_to_send)
        print("Item updated")

    def delete_item(self):
        name = input("Write the name of the product that will be deleted: ")

        data_to_send = (name,)

        query = sql.SQL("DELETE FROM item WHERE name = %s;")

        self.supermarket.execute_command(query, data_to_send)
        print("Item deleted")
    
    def search_item(self):
        name = input("Write the name of the product to be searched: ")

        data_to_send = (name,)

        query = sql.SQL("SELECT * FROM item WHERE name = %s;")

        self.supermarket.execute_command(query, data_to_send)

        result = self.supermarket.cur.fetchall()

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

        self.supermarket.execute_command(query1)

        result1 = self.supermarket.cur.fetchall()

        print("The quantity of items stored is: ",result1[0][0])
        
        self.supermarket.execute_command(query2)

        result2 = self.supermarket.cur.fetchall()

        print("The total sum of values in items is: ", result2[0][0])

        self.supermarket.execute_command(query3)

        result3 = self.supermarket.cur.fetchall()

        if result3:
            for i in result3:
                print(i)
            print("Items found")
        else:
            print("Items not found")

    def generate_stock_report(self):
        print(f"\n{'='*50}")
        print(f"{'STOCK REPORT':^50}")
        print(f"{'='*50}\n")

        summary_query = sql.SQL("SELECT * FROM general_stock_report;")
        self.supermarket.execute_command(summary_query)
        
        report_data = self.supermarket.cur.fetchone()

        if report_data:
            print(f"{' GENERAL STOCK SUMMARY ':-^50}")
            print(f"Unique items registered: {report_data[0]}")
            print(f"Total units in stock: {report_data[1]}")
            print(f"Total stock value: R$ {report_data[2]:.2f}")
            print(f"Average price per item: R$ {report_data[3]:.2f}")
            print(f"{'-'*50}\n")
        else:
            print("Could not generate report. The stock might be empty.")

    def EndConnection(self):
        self.supermarket.end_connection()
        print("Connection with the database endend")

