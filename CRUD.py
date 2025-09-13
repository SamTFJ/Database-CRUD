# CRUD.py
from manager import GerenciadorProduto
from models import Produto

def prompt_int(prompt: str, default: int = 0) -> int:
    while True:
        try:
            val = input(prompt)
            if val.strip() == "":
                return default
            return int(val)
        except ValueError:
            print("Please enter a valid integer.")

def prompt_float(prompt: str, default: float = 0.0) -> float:
    while True:
        try:
            val = input(prompt)
            if val.strip() == "":
                return default
            return float(val)
        except ValueError:
            print("Please enter a valid number (e.g., 12.50).")

class CRUD:
    def __init__(self):
        self.gestor = GerenciadorProduto()

    def run(self):
        while True:
            print("\n                MENU")
            print("|=================================|")
            print("|     1 - Insert new item         |")
            print("|     2 - Update item             |")
            print("|     3 - Delete item             |")
            print("|     4 - Search for item         |")
            print("|     5 - Show all items          |")
            print("|     6 - Report by category      |")
            print("|     7 - Save and exit           |")
            print("|=================================|")

            choice = input("Select an option: ").strip()

            try:
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
                    self.report_by_category()
                elif choice == '7':
                    self.EndConnection()
                    print("Exiting application...")
                    break
                else:
                    print("Invalid option. Please try again.")
            except Exception as e:
                print("An error occurred:", e)

            if choice != '7':
                input("Press Enter to continue...")

    def insert_item(self):
        name = input("Write the name of the product: ").strip()
        value = prompt_float("Write the value of the product (EX: 20.5): ")
        quantity = prompt_int("Write the quantity (EX: 10): ")
        category = input("Write the category (optional): ").strip() or None

        prod = Produto(name=name, value=value, quantity=quantity, category=category)
        try:
            new_id = self.gestor.insert(prod)
            print(f"Item inserted with id: {new_id}")
        except Exception as e:
            print("Failed to insert item:", e)

    def update_item(self):
        name = input("Write the name of the product that will be updated: ").strip()
        print("Enter new values (leave empty to cancel):")
        new_name = input("Write the new name of the product: ").strip()
        if not new_name:
            print("Update canceled (empty name).")
            return
        new_value = prompt_float("Write the new value of the product: ")
        new_quantity = prompt_int("Write the new quantity: ")
        new_category = input("Write the new category (optional): ").strip() or None

        new_prod = Produto(name=new_name, value=new_value, quantity=new_quantity, category=new_category)
        try:
            updated = self.gestor.update_by_name(name, new_prod)
            print(f"Records updated: {updated}")
        except Exception as e:
            print("Failed to update:", e)

    def delete_item(self):
        name = input("Write the name of the product that will be deleted: ").strip()
        confirm = input(f"Are you sure you want to delete all items named '{name}'? (y/N): ").lower()
        if confirm != 'y':
            print("Operation canceled.")
            return
        try:
            deleted = self.gestor.delete_by_name(name)
            print(f"Records deleted: {deleted}")
        except Exception as e:
            print("Failed to delete:", e)

    def search_item(self):
        name = input("Write the name of the product to be searched: ").strip()
        try:
            results = self.gestor.get_by_name(name)
            if results:
                for p in results:
                    print(p)
                print("Item(s) found")
            else:
                print("Item not found")
        except Exception as e:
            print("Error during search:", e)

    def list_collection(self):
        try:
            qtd = self.gestor.count()
            total = self.gestor.total_value()
            print("The quantity of items stored is:", qtd)
            print("The total inventory value is:", total)
            produtos = self.gestor.list_all()
            if produtos:
                for p in produtos:
                    print(p)
                print("Items found")
            else:
                print("Items not found")
        except Exception as e:
            print("Error listing collection:", e)

    def report_by_category(self):
        try:
            report = self.gestor.report_by_category()
            if not report:
                print("No data for the report.")
                return
            print("{:<30} {:>8} {:>15} {:>10}".format("Category", "Items", "Total Value", "Quantity"))
            print("-" * 70)
            for cat, qty_items, total_value, total_quantity in report:
                print("{:<30} {:>8} {:>15.2f} {:>10}".format(cat, qty_items, total_value, total_quantity))
        except Exception as e:
            print("Error generating report:", e)

    def EndConnection(self):
        try:
            self.gestor.db.end_connection()
            print("Connection with the database ended")
        except Exception as e:
            print("Error while closing connection:", e)

if __name__ == "__main__":
    crud = CRUD()
    crud.run()
