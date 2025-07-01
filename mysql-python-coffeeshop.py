#!/usr/bin/env python3
import mysql.connector

class Coffee_Shop:
    def __init__ (self, name):
        self.name = name
        self.sales = 0
        self.numbers_served = 0
        self.admin_password = "uno1234"
        self.menu_list = ["coffee", "food", "top10books", "manga"]

        self.coffee_menu = {
            "cappuccino": {"author": "", "price": 3.50, "stock": 300},
            "latte": {"author": "", "price": 3.50, "stock": 300},
            "americano": {"author": "", "price": 3.50, "stock": 300},
            "black coffee": {"author": "", "price": 3.50, "stock": 300},
            "espresso": {"author": "", "price": 3.50, "stock": 300},
            "macchiato": {"author": "", "price": 3.50, "stock": 300},
            "flat white": {"author": "", "price": 3.50, "stock": 300},
            "tea": {"author": "", "price": 3.50, "stock": 300},
            "hot chocolate": {"author": "", "price": 3.50, "stock": 300},
        }

        self.food_menu = {
            "croissant": {"author": "", "price": 2.00, "stock": 50},
            "danish": {"author": "", "price": 2.90, "stock": 20},
            "gf croissant": {"author": "", "price": 2.50, "stock": 50},
            "muffin": {"author": "", "price": 3.90, "stock": 50},
            "scone": {"author": "", "price": 3.50, "stock": 50},
            "brownie": {"author": "", "price": 3.00, "stock": 50},
            "granola bar": {"author": "", "price": 2.50, "stock": 50},
            "fresh fruit": {"author": "", "price": 4.00, "stock": 50},
            "veggie panini": {"author": "", "price": 5.50, "stock": 50},
            "vegan panini": {"author": "", "price": 4.50, "stock": 50},
            "veggie wrap": {"author": "", "price": 4.00, "stock": 50},
        }

        self.top10books_menu = {
            "dream count": {"author": "Chimamanda Ngozi Adichie", "price": 15.00, "stock": 5},
            "atmosphere, a love story": {"author": "Taylor Jenkins Reid", "price": 20.00, "stock": 0},
            "we do not part": {"author": "Han Kang", "price": 18.00, "stock": 1},
            "the land of sweet forever": {"author": "Harper Lee", "price": 10.00, "stock": 0},
            "three days in june": {"author": "Anne Tyler", "price": 14.99, "stock": 2},
            "universality: signed edition": {"author": "Natasha Brown", "price": 12.99, "stock": 3},
            "we all live here": {"author": "Jojo Moyes", "price": 16.99, "stock": 2},
            "the emperor of gladness": {"author": "Ocean Vuong", "price": 17.99, "stock": 3},
            "the secrets of secrets": {"author": "Dan Brown", "price": 12.50, "stock": 0},
            "spring": {"author": "Michael Morurgo", "price": 16.99, "stock": 1},
            "source code": {"author": "Bill Gates", "price": 19.99, "stock": 1},
        }

        self.manga_menu = {
            "one piece vol 105": {"author": "Eiichiro Oda", "price": 7.50, "stock": 15},
            "berzerk vol 1": {"author": "Kentaro Miura", "price": 30.00, "stock": 3},
            "attack on titan": {"author": "Hajime Isayama", "price": 12.00, "stock": 10},
            "hunter x hunter vol 38": {"author": "Yoshihiro Togashi", "price": 15.00, "stock": 2},
            "naruto vol 72": {"author": "Masashi Kishimoto", "price": 15.00, "stock": 7},
        }

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="booknorder"
        )
        self.cursor = self.db.cursor(dictionary=True)
        self.sync_all_menus()

    def sync_all_menus(self):
        self.sync_menu("coffee", self.coffee_menu)
        self.sync_menu("food", self.food_menu)
        self.sync_menu("top10books", self.top10books_menu)
        self.sync_menu("manga", self.manga_menu)

    def sync_menu(self, menu_type, items):
        for name, details in items.items():
            self.cursor.execute(f"SELECT * FROM {menu_type}_menu WHERE name = %s", (name,))
            result = self.cursor.fetchone()
            if result:
                if menu_type in ["top10books", "manga"]:
                    author = details.get("author", "")
                    self.cursor.execute(
                        f"UPDATE {menu_type}_menu SET price = %s, stock = %s, author = %s WHERE name = %s",
                        (details["price"], details["stock"], author, name)
                    )
                else:
                    self.cursor.execute(
                        f"UPDATE {menu_type}_menu SET price = %s, stock = %s WHERE name = %s",
                        (details["price"], details["stock"], name)
                    )
            else:
                if menu_type in ["top10books", "manga"]:
                    author = details.get("author", "")
                    self.cursor.execute(
                        f"INSERT INTO {menu_type}_menu (name, price, stock, author) VALUES (%s, %s, %s, %s)",
                        (name, details["price"], details["stock"], author)
                    )
                else:
                    self.cursor.execute(
                        f"INSERT INTO {menu_type}_menu (name, price, stock) VALUES (%s, %s, %s)",
                        (name, details["price"], details["stock"])
                    )
        self.db.commit()

    def display_menu(self, menu):
        for item, details in menu.items():
            price = details["price"]
            author = details.get("author", "")
            author_display = f", {author.lower()}" if author else ""
            print(f" - {item.title()}{author_display} (£{price:.2f})")

    def get_price(self, item_name):
        for menu in [self.coffee_menu, self.food_menu, self.top10books_menu, self.manga_menu]:
            if item_name in menu:
                return menu[item_name]["price"]
        return 0

    def get_table_name(self, menu_dict):
        if menu_dict is self.coffee_menu:
            return "coffee_menu"
        elif menu_dict is self.food_menu:
            return "food_menu"
        elif menu_dict is self.top10books_menu:
            return "top10books_menu"
        elif menu_dict is self.manga_menu:
            return "manga_menu"
        return ""

    def customer_order(self):
        while True:
            name = input("Welcome to Bookend Coffee! What is your name? (type 'admin' for admin access, EXIT to cancel): ").strip()
            if name.lower() == "admin":
                self.admin_panel()
                return
            elif name.lower() == "exit":
                print("Goodbye.")
                return
            else:
                print(f"\nHi {name.title()}. What would you like to order?")

            total = 0
            items = []

            while True:
                choice = input("[1] Coffee | [2] Food | [3] Books | [4] Manga | [5] Pay | [6] EXIT: ").strip().lower()
                if choice == '5':
                    self.take_payment(total, items)
                    return
                elif choice == '6':
                    print("Goodbye!")
                    return

                menu_map = {
                    '1': self.coffee_menu,
                    '2': self.food_menu,
                    '3': self.top10books_menu,
                    '4': self.manga_menu
                }

                if choice in menu_map:
                    menu = menu_map[choice]
                    print()
                    self.display_menu(menu)
                    item = input("Enter item name: ").strip().lower()
                    if item in menu and menu[item]["stock"] > 0:
                        price = menu[item]["price"]
                        menu[item]["stock"] -= 1
                        self.cursor.execute(
                            f"UPDATE {self.get_table_name(menu)} SET stock = %s WHERE name = %s",
                            (menu[item]["stock"], item))
                        self.db.commit()
                        total += price
                        items.append(item)
                        print(f"{item.title()} added to order.")
                    else:
                        print("Item not found or out of stock.")
                else:
                    print("Invalid option.")
                    continue

                con = input("Would you like to order more? [Y]/[N]: ").strip().lower()
                if con == 'n':
                    self.take_payment(total, items)
                    return
                elif con != 'y':
                    print("Invalid input. Continuing to menu...")

    def take_payment(self, total, items):
        if total == 0:
            print("No items in your order. Please try again.")
            return

        print("\nOrder Summary:")
        for item in items:
            print(f" - {item.title()}")
        print(f"Total: £{total:.2f}")

        while True:
            try:
                payment = float(input("Enter payment amount: £"))
                if payment >= total:
                    change = payment - total
                    print(f"Payment accepted. Change: £{change:.2f}")
                    self.sales += total
                    self.numbers_served += 1
                    print("Thank you for your order!\n")
                    return
                else:
                    print("Insufficient funds. Try again.")
            except ValueError:
                print("Invalid input. Enter a number.")

    def admin_panel(self):
        password = input("Enter admin password: ")
        if password != self.admin_password:
            print("Incorrect password.")
            return

        while True:
            print("\nAdmin Panel Options:")
            choice = input("[1] Add Stock | [2] Apply Discount | [3] Add Item | [4] Remove Item | [5] View Stock | [6] Exit Admin: ").strip()
            if choice == '1':
                self.admin_add_stock()
            elif choice == '2':
                self.admin_apply_discount()
            elif choice == '3':
                self.admin_add_item()
            elif choice == '4':
                self.admin_remove_item()
            elif choice == '5':
                self.view_stock_levels()
            elif choice == '6':
                print("Exiting admin panel.\n")
                return
            else:
                print("Invalid option.")

    def admin_add_stock(self):
        while True:
            menu_type = input("Select menu [coffee/food/top10books/manga] [E] Exit: ").strip().lower()
            if menu_type == "e":
                break
            if menu_type not in self.menu_list:
                print("Enter a valid menu type.")
                continue
            menu = self.get_menu_by_type(menu_type)
            item = input("Enter item name to restock: ").strip().lower()
            if item in menu:
                try:
                    amount = int(input("Enter amount to add: "))
                    menu[item]["stock"] += amount
                    self.cursor.execute(
                        f"UPDATE {menu_type}_menu SET stock = %s WHERE name = %s",
                        (menu[item]["stock"], item))
                    self.db.commit()
                    print(f"{amount} units added to {item.title()}.")
                except ValueError:
                    print("Invalid amount.")
            else:
                print("Item not found.")

    def admin_apply_discount(self):
        while True:
            menu_type = input("Select menu to discount [coffee/food/top10books/manga] [E] Exit: ").strip().lower()
            if menu_type == 'e':
                break
            if menu_type not in self.menu_list:
                print("Invalid menu.")
                continue
            menu = self.get_menu_by_type(menu_type)
            item = input("Enter item name: ").strip().lower()
            if item in menu:
                try:
                    percent = float(input("Enter discount percentage: "))
                    old_price = menu[item]["price"]
                    menu[item]["price"] *= (1 - percent / 100)
                    print(f"{item.title()} discounted from £{old_price:.2f} to £{menu[item]['price']:.2f}")
                    self.sync_menu(menu_type, menu)
                except ValueError:
                    print("Invalid percentage.")
            else:
                print("Item not found.")

    def admin_add_item(self):
        while True:
            menu_type = input("Select menu to add to [coffee/food/top10books/manga] [E] Exit: ").strip().lower()
            if menu_type == 'e':
                break
            if menu_type not in self.menu_list:
                print("Invalid menu.")
                continue

            item = input("Enter new item name: ").strip().lower()
            try:
                price = float(input("Enter item price: "))
                stock = int(input("Enter stock amount: "))
            except ValueError:
                print("Invalid input.")
                continue

            author = input("Enter author name (leave blank if not applicable): ").strip()
            menu = self.get_menu_by_type(menu_type)
            menu[item] = {"author": author, "price": price, "stock": stock}
            self.sync_menu(menu_type, menu)
            print(f"{item.title()} added successfully.")

    def admin_remove_item(self):
        while True:
            menu_type = input("Select menu to remove from [coffee/food/top10books/manga] [E] Exit: ").strip().lower()
            if menu_type == "e":
                break
            if menu_type not in self.menu_list:
                print("Invalid menu.")
                continue
            menu = self.get_menu_by_type(menu_type)
            item = input("Enter item name to remove: ").strip().lower()
            if item in menu:
                del menu[item]
                self.cursor.execute(
                    f"DELETE FROM {menu_type}_menu WHERE name = %s", (item,))
                self.db.commit()
                print(f"{item.title()} removed.")
            else:
                print("Item not found.")

    def get_menu_by_type(self, menu_type):
        return {
            "coffee": self.coffee_menu,
            "food": self.food_menu,
            "top10books": self.top10books_menu,
            "manga": self.manga_menu,
        }.get(menu_type, {})

    def view_stock_levels(self):
        print("\n--- Stock Levels ---")
        for category, menu in [
            ("coffee", self.coffee_menu),
            ("food", self.food_menu),
            ("top10books", self.top10books_menu),
            ("manga", self.manga_menu)
        ]:
            print(f"\n{category.title()} Menu:")
            for item, data in menu.items():
                print(f" - {item.title()}: {data['stock']} in stock")


# Start the program
shop = Coffee_Shop("Bookend Coffee")
shop.customer_order()