import json
import bcrypt
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font

class Varasto():
    def __init__(self):
        ## Variables for filepaths
        self.PRODUCTS_FILE = './data/products.json'
        self.INVENTORY_FILE = './data/inventory.json'
        self.USER_FILE = './data/users.json'
        self.INVENTORY_HISTORY_FILE = './data/inventory_history.json'
        ## While self.running is true the app will run
        self.running = True
        self.main_menu_nav()

    ## Function to open a json file
    def openfile(self, filename):
        ## Opening the json file as read-only
        with open(filename, 'r') as json_file:
            ## Save the json file as a dictionary
            file = json.load(json_file)
            json_file.close()
            ## Returns the dictionary
            return file
        
    ## Function to write into a json file
    def write_json(self, filename, data):
        ## Opening the json file to append it
        with open(filename, 'w') as json_file:
            ## Dumping the dictionary into the json file
            json.dump(data, json_file, indent=4)

    ## The navigation for the menu
    def main_menu_nav(self):
        print(f"----- MAIN MENU -----")
        print(f"1. Products")
        print(f"2. Inventory")
        print(f"3. Analytics")
        print(f"4. Users")
        print(f"5. Exit\n")
        choice = input("Select option: ")
        self.menu_option_handling(choice)

## 1. PRODUCTS 

    ## The navigation for the submenu for products
    def products_menu_nav(self):
        print(f"----- PRODUCTS -----")
        print(f"1. Add product")
        print(f"2. Edit product")
        print(f"3. Back\n")

    ## Function to add a new product to the json file
    def add_product(self):
        ## Loading the existing json file into a variable (datafile)
        product_data = self.openfile(self.PRODUCTS_FILE)
        ## Assigning a product ID based on the length of the json file
        product_id = len(product_data)+1
        ## Input for the product name
        product_name = input("Product name: ")
        ## Creating a new, empty entry in the datafile
        product_data[product_id] = {}
        ## Assigns the product name from the input into the datafile
        product_data[product_id]["product_name"] = product_name
        ## Dumps the datafile into the json file
        self.write_json(self.PRODUCTS_FILE, product_data)

    ## Function to list existing products
    def list_products(self):
        ## Loading existing json file into a variable (datafile)
        product_data = self.openfile(self.PRODUCTS_FILE)
        ## Prints the product ID and product name
        for product in product_data:
            print(f"{product} {product_data[product]["product_name"]}")
        print(f"Enter 'b' to return")
        ## Asking for product ID so the program knows which line needs to be edited
        input_to_edit = input("Enter product ID to edit: ")
        ## Checking if input_to_edit is "b", which means to return to the previous menu
        if input_to_edit == "b":
            pass
        else:
            ## Asking for new product name
            edited_input = input("New name of the product: ")
            ## Assigns the new product  name into the datafile
            product_data[input_to_edit]["product_name"] = edited_input
            ## Dumps the datafile into the json file and overwrites it
            self.write_json(self.PRODUCTS_FILE, product_data)

## 2. INVENTORY

    ## The navigation for the submenu for users
    def inventory_menu_nav(self):
        print(f"----- INVENTORY -----")
        print(f"1. Add quantity")
        print(f"2. Remove quantity")
        print(f"3. Show inventory")
        print(f"4. Back\n")

    ## Function to add new inventory
    def add_inventory(self):
        ## Loading the inventory json into a dictionary
        inventory_data = self.openfile(self.INVENTORY_FILE)
        ## Loading the products json into a dictionary
        products_data = self.openfile(self.PRODUCTS_FILE)
        ## Loading the inventory history json into a dictionary
        inventory_history_data = self.openfile(self.INVENTORY_HISTORY_FILE)
        ## Creating timestamp
        current_date = datetime.now().date().isoformat()
        ## Creating an ID for the inventory history entry
        inventory_history_id = len(inventory_history_data)
        ## Prints the product ID and name
        for product in products_data:
            print(f"{product} {products_data[product]["product_name"]}")
        print("Enter 'b' to return")
        ## Asking which product needs to be added to the inventory
        input_to_edit = input("Enter product ID to add quantity: ")
        ## if input is "b" user gets sent back to the previous menu
        if input_to_edit == "b":
            pass
        else:
            ## Asking for the quantity to be added
            quantity_add = int(input("Add quantity: "))
            ## If the product already has inventory it's simply getting added to the existing one
            if input_to_edit in inventory_data:
                inventory_data[input_to_edit]["quantity"] += quantity_add
                ## Creating new instance for the inventory history data
                inventory_history_data[inventory_history_id] = {}
                ## Addint product ID
                inventory_history_data[inventory_history_id]["product_id"] = input_to_edit
                ## Adding product name
                inventory_history_data[inventory_history_id]["product_name"] = products_data[input_to_edit]["product_name"]
                ## Adding quantity which was added
                inventory_history_data[inventory_history_id]["quantity"] = quantity_add
                ## Adding current date
                inventory_history_data[inventory_history_id]["date"] = current_date
                ## Adding current week
                inventory_history_data[inventory_history_id]["week"] = datetime.today().isocalendar().week
                ## Adding movement type
                inventory_history_data[inventory_history_id]["movement"] = "add"

            ## If the product is not already in the inventory, a new entry is made
            else:
                ## Creating empty inventory for the respective product
                inventory_data[input_to_edit] = {}
                ## Adding name to the inventory
                inventory_data[input_to_edit]["product_name"] = products_data[input_to_edit]["product_name"]
                ## Adding new inventory history entry
                inventory_history_data[inventory_history_id] = {}
                ## Adding product ID to the inventory history
                inventory_history_data[inventory_history_id]["product_id"] = input_to_edit
                ## Adding product name to the inventory history
                inventory_history_data[inventory_history_id]["product_name"] = products_data[input_to_edit]["product_name"]
                ## Adding quantity to the inventory and inventory history
                inventory_data[input_to_edit]["quantity"] = quantity_add
                ## Adding quantity
                inventory_history_data[inventory_history_id]["quantity"] = quantity_add
                ## Adding current date
                inventory_history_data[inventory_history_id]["date"] = current_date
                ## Adding current week
                inventory_history_data[inventory_history_id]["week"] = datetime.today().isocalendar().week
                ## Adding movement type
                inventory_history_data[inventory_history_id]["movement"] = "add"
        ## Dumps the datafile into the json file and overwrites it
        self.write_json(self.INVENTORY_FILE, inventory_data)          
        ## Dumps the datafile into the json file and overwrites it
        self.write_json(self.INVENTORY_HISTORY_FILE, inventory_history_data)  
        
    ## Function to remove quantity from the inventory
    def remove_inventory(self):
        ## Loading the inventory json into a dictionary
        inventory_data = self.openfile(self.INVENTORY_FILE)
        ## Loading the inventory history json into a dictionary
        inventory_history_data = self.openfile(self.INVENTORY_HISTORY_FILE)
        ## Creating timestamp
        current_date = datetime.now().date().isoformat()
        ## Creating an ID for the inventory history entry
        inventory_history_id = len(inventory_history_data)
        ## Printing current inventory and quantity
        for inventory in inventory_data:
            print(f"{inventory} {inventory_data[inventory]["product_name"]} -> {inventory_data[inventory]["quantity"]}")
        print("Enter 'b' to return")
        input_to_edit = input("Enter product ID to remove quantity: ")
        ## Checking if user wants to go to the previous menu
        if input_to_edit == "b":
            pass
        else:
            ## Asking quantity that needs to be removed from the current inventory
            quantity_remove = int(input("Remove quantity: "))
            ## Removing quantity from the current inventory
            inventory_data[input_to_edit]["quantity"] -= quantity_remove
            ## Creating new instance for the inventory history data
            inventory_history_data[inventory_history_id] = {}
            ## Adding product ID
            inventory_history_data[inventory_history_id]["product_id"] = input_to_edit
            ## Adding product name
            inventory_history_data[inventory_history_id]["product_name"] = inventory_data[input_to_edit]["product_name"]
            ## Adding quantity which was removed
            inventory_history_data[inventory_history_id]["quantity"] = quantity_remove
            ## Adding current date
            inventory_history_data[inventory_history_id]["date"] = current_date
            ## Adding current week
            inventory_history_data[inventory_history_id]["week"] = datetime.today().isocalendar().week
            ## Adding movement type
            inventory_history_data[inventory_history_id]["movement"] = "remove"
        ## Dumps the datafile into the json file and overwrites it
        self.write_json(self.INVENTORY_FILE, inventory_data)  
        ## Dumps the datafile into the json file and overwrites it
        self.write_json(self.INVENTORY_HISTORY_FILE, inventory_history_data)

    ## Function to list the current inventory
    def list_inventory(self):
        ## Loading the inventory json into a dictionary
        inventory_data = self.openfile(self.INVENTORY_FILE)
        ## Printing current inventory and quantity
        for inventory in inventory_data:
            print(f"{inventory} {inventory_data[inventory]["product_name"]} -> {inventory_data[inventory]["quantity"]}")
        print("Enter 'b' to return")
        ## Asking for input to see if user wants to go to the previous menu
        input_to_return = input("Confirm returning with 'b': ")
        ## If input is 'b' user goes to the previous menu
        if input_to_return == 'b':
            pass

## 3. ANALYTICS

    ## The navigation for the sebmenu analytics
    def analytics_menu_nav(self):
        print(f"----- ANALYTICS -----")
        print(f"1. Annual report")
        print(f"2. Monthly report")
        print(f"3. Weekly report")
        print(f"4. Daily report")
        print(f"5. Custom report")
        print(f"6. Back\n")

    ## Function to filter the data needed to create a report by year
    def year_report_filtering(self):
        ## Loading the inventory json into a dictionary
        inventory_history_data = self.openfile(self.INVENTORY_HISTORY_FILE)
        ## Starting a while loop to validate the input for the year
        while True:
            ## Trying to validate input
            try:
                ## Asking for which year the report needs to account for
                input_year = input("Enter year: ")
                ## If input is not a number the loop continues
                if int(input_year):
                    break
                ## Message printing if input is invalid
                print("That's not a number")
            ## Catching Valueerrors
            except ValueError:
                print("Invalid input!")
        ## Creating an object to save the relevant data for the report
        relevant_data = {}
        ## For loop to sort the relevant data
        for entry in inventory_history_data:
            if inventory_history_data[entry]["date"][:4] == input_year:
                relevant_data[entry] = inventory_history_data[entry]
        ## Returns the object with the relevant data
        self.excel_report_creation(relevant_data, "Annual report")

    ## Function to filter the data needed to create a report by month
    def month_report_filtering(self):
        ## Calling year_report_filtering() and assigning it to a variable
        year_data = self.year_report_filtering()
        ## Starting a while loop to validate the input for the month
        while True:
            ## Trying to validate input
            try:
                ## Asking for which month the report needs to account for
                input_month = input("Enter month (1-12): ")
                ## If input is not a number and not between 1 and 12 
                # the loop continues
                if int(input_month) > 0 and int(input_month) < 13:
                    break
                ## Message printing if input is invalid
                print("Input needs to be between 1 and 12!")
            ## Catching Valueerrors
            except ValueError:
                print("Invalid number!")
        ## If input length is not two-digits it adds a "0" in the front, so it's
        # possible to match them with year_data
        if len(input_month) < 2:
            input_month = "0" + input_month
        ## Creating empty relevant_data
        relevant_data = {}
        ## Iterating through year_data and dump the matching data into relevant_data
        for entry in year_data:
            if year_data[entry]["date"][5:7] == input_month:
                relevant_data[entry] = year_data[entry]
        ## Returning the relevant data for the report
        self.excel_report_creation(relevant_data, "Monthly report")

    ## Function to filter the data needed to create a report by week
    def week_report_filtering(self):
        ## Calling year_report_filtering() and assigning it to a variable
        year_data = self.year_report_filtering()
        ## Starting a while loop to validate the input for the month
        while True:
            ## Trying to validate input
            try:
                ## Asking for which month the report needs to account for
                input_week = input("Enter week (1-52): ")
                ## If input is not a number and not between 1 and 52 
                # the loop continues
                if int(input_week) > 0 and int(input_week) < 53:
                    break
                ## Message printing if input is invalid
                print("Input needs to be between 1 and 52!")
            ## Catching Valueerrors
            except ValueError:
                print("Invalid number!")
        ## Creating empty relevant_data
        relevant_data = {}
        ## Iterating through year_data and dump the matching data into relevant_data
        for entry in year_data:
            if year_data[entry]["week"] == int(input_week):
                relevant_data[entry] = year_data[entry]
        ## Returning the relevant data for the report
        self.excel_report_creation(relevant_data, "Weekly report")

    ## Function to filter the data needed to create a report by day
    def day_report_filtering(self):
        ## Calling year_report_filtering() and assigning it to a variable
        month_data = self.month_report_filtering()
        ## Starting a while loop to validate the input for the month
        while True:
            ## Trying to validate input
            try:
                ## Asking for which month the report needs to account for
                input_day = input("Enter day (1-31): ")
                ## If input is not a number and not between 1 and 31 
                # the loop continues
                if int(input_day) > 0 and int(input_day) < 32:
                    break
                ## Message printing if input is invalid
                print("Input needs to be between 1 and 32!")
            ## Catching Valueerrors
            except ValueError:
                print("Invalid number!")
        ## If input length is not two-digits it adds a "0" in the front, so it's
        # possible to match them with month_data
        if len(input_day) < 2:
            input_day = "0" + input_day
        ## Creating empty relevant_data
        relevant_data = {}
        ## Iterating through month_data and dump the matching data into relevant_data
        for entry in month_data:
            if month_data[entry]["date"][8:10] == input_day:
                relevant_data[entry] = month_data[entry]
        ## Returning the relevant data for the report
        self.excel_report_creation(relevant_data, "Daily report")

    ## Function to create own timespan to extract data for a report
    def custom_report_filtering(self):
        ## Loading the inventory json into a dictionary
        inventory_history_data = self.openfile(self.INVENTORY_HISTORY_FILE)
        ## Asking for input on which year to start the report in a loop
        while True:
            ## Try input until its valid
            try:
                input_year_start = int(input("Enter start year: "))
                ## If input_year_start is int the loop breaks
                if int(input_year_start):
                    break
                print("Invalid number!")
            ## Throw valueerror when something went wrong with the input
            except ValueError:
                print("Invalid input!")
        ## Asking for input on which month to start the report in a loop
        while True:
            ## Try input until its valid
            try:
                input_month_start = int(input("Enter start month: "))
                ## If input_month_start is int and between 0 and 13 loop breaks
                if int(input_month_start) > 0 and int(input_month_start) < 13:
                    break
                print("Invalid number!")
            ## Throw valueerror when something went wrong with the input
            except ValueError:
                print("Invalid input!")
        ## Asking for input on which day to start the report in a loop
        while True:
            ## Try input until its valid
            try:
                input_day_start = int(input("Enter start day: "))
                ## If input_day_start is int and between 0 and 32 loop breaks
                if int(input_day_start) > 0 and int(input_day_start) < 32:
                    break
                print("Invalid number!")
            ## Throw valueerror when something went wrong with the input
            except ValueError:
                print("Invalid input!")
        ## Asking for input on which year to end the report in a loop
        while True:
            ## Try input until its valid
            try:
                input_year_end = int(input("Enter end year: "))
                ## If input_year_start is int the loop breaks
                if int(input_year_end):
                    break
                print("Invalid number!")
            ## Throw valueerror when something went wrong with the input
            except ValueError:
                print("Invalid input!")
        ## Asking for input on which month to end the report in a loop
        while True:
            ## Try input until its valid
            try:
                input_month_end = int(input("Enter end month: "))
                ## If input_month_start is int and between 0 and 13 loop breaks
                if int(input_month_end) > 0 and int(input_month_end) < 13:
                    break
                print("Invalid number!")
            ## Throw valueerror when something went wrong with the input
            except ValueError:
                print("Invalid input!")
        ## Asking for input on which day to end the report in a loop
        while True:
            ## Try input until its valid
            try:
                input_day_end = int(input("Enter end day: "))
                ## If input_day_start is int and between 0 and 32 loop breaks
                if int(input_day_end) > 0 and int(input_day_end) < 32:
                    break
                print("Invalid number!")
            ## Throw valueerror when something went wrong with the input
            except ValueError:
                print("Invalid input!")
        ## Creating start_date as a datetime object
        start_date = datetime(input_year_start, input_month_start, input_day_start)
        ## Creating end_date as a datetime object
        end_date = datetime(input_year_end, input_month_end, input_day_end)
        ## Declaring relevant_data as a variable
        relevant_data = {}
        ## Looping through the inventory_history_data to find matching entries
        for entry in inventory_history_data:
            ## Declaring the entry_year based off of the string
            entry_year = int(inventory_history_data[entry]["date"][:4])
            ## Declaring the entry_month based off of the string
            entry_month = int(inventory_history_data[entry]["date"][5:7])
            ## Declaring the entry_day based off of the string
            entry_day = int(inventory_history_data[entry]["date"][8:10])
            ## Creating current_date as a datetime object
            current_date = datetime(entry_year, entry_month, entry_day)
            ## Comparing current_date (entry) with the start_date and end_date
            if start_date <= current_date <= end_date:
                ## If it fullfills the criteria it's added to relevant_data
                relevant_data[entry] = inventory_history_data[entry]

        self.excel_report_creation(relevant_data, "Custom report")

    ## Function to generate the actual report as an excel file
    def excel_report_creation(self, year_data, title):
        ## Creating a Workbook
        wb = Workbook()
        ## Setting worksheet as active
        ws = wb.active
        ## Giving the worksheet a title
        ws.title = title
        ## Create headers in the excel file
        headers = ["Product ID", "Product Name", "Quantity", "Date"]
        ## Append the headers to the worksheet
        ws.append(headers)
        ## Set the headers as bold
        for cell in ws[1]:
            cell.font = Font(bold=True)
        ## Iterating through year_data
        for entry in year_data:
            ## If the entry in year_data has "remove" as "movement" it's being set
            # to a negative number
            if year_data[entry]["movement"] == "remove":
                year_data[entry]["quantity"] = -abs(year_data[entry]["quantity"])
            ## Assigning year_data[entry] to item
            item = year_data[entry]
            ## Appending the data to the headers in the worksheet
            ws.append([
                item["product_id"],
                item["product_name"],
                item["quantity"],
                item["date"],
            ])
        ## Saving the Workbook
        title_split = title.split()
        wb.save(f"{title_split[0]}_{title_split[1]}.xlsx")

## 4. USERS
    
    ## The navigation for the submenu for users
    def users_menu_nav(self):
        print(f"----- USERS -----")
        print(f"1. Create User")
        print(f"2. Edit User")
        print(f"3. Back\n")

    ## Function to hash passwords
    def hash_password(self, plain_password):
        hashed = bcrypt.hashpw(
            plain_password.encode("utf-8"),
            bcrypt.gensalt()
        )
        return hashed.decode("utf-8")

    ## Function to add a new user
    def add_user(self):
        ## Loading users.json into a dictionary
        user_data = self.openfile(self.USER_FILE)
        ## Assigning new user ID based on the users dictionary length
        user_id = len(user_data)+1
        ## Asking for input for the username
        user_name = input("Username: ")
        ## Asking for input for the password
        user_password = input("Password: ")
        ## Asking for inoput for the user role
        user_role = input("User role: ")
        ## Hashing the password which was provided
        hashed_user_password = self.hash_password(user_password)
        ## Creating a new entry in the users dictionary
        user_data[user_id] = {}
        ## Assigning name to the user in the dictionary
        user_data[user_id]["name"] = user_name
        ## Assigning hashed password to the user in the dictionary
        user_data[user_id]["password"] = hashed_user_password
        ## Assigning role to the user in the dictionary
        user_data[user_id]["role"] = user_role
        ## Dumping the dictionary to the users.json file
        self.write_json(self.USER_FILE, user_data)

    ## Functino to list all users to edit them
    def list_users(self):
        ## Loading users.json into a dictionary
        user_data = self.openfile(self.USER_FILE)
        ## Printing all user IDs with their username
        for user_id in user_data:
            print(f"{user_id} {user_data[user_id]["name"]}")
        print(f"Enter 'b' to return")
        ## Asking for product ID so the program knows which line needs to be edited
        input_to_edit = input("Enter user ID to edit: ")
        ## Checks if the user wants to go back or which user needs to be edited
        if input_to_edit == "b":
            pass
        else:
            ## Asking for new username
            edited_username = input("New username: ")
            ## Asking for new password
            edited_password = input("New password: ")
            ## Asking for new role
            edited_role = input("New role: ")
            ## Assigning new username to the dictinoary
            user_data[input_to_edit]["name"] = edited_username
            ## Assigning hashed password to the dictionary
            user_data[input_to_edit]["password"] = self.hash_password(edited_password)
            ## Assigning new role to the dictinoary
            user_data[input_to_edit]["role"] = edited_role
            ## Dumping the dictionary to the users.json
            self.write_json(self.USER_FILE, user_data)

    ## Function to handle menu inputs to navigate through the options
    def menu_option_handling(self, choice):
        ## Menu input 1 to display product information
        if choice == "1":
            ## Loading the submenu for products
            self.products_menu_nav()
            ## Asking for new input to navigate through the submenu
            sub_choice_1 = input("Select option: ")
            ## While sub_choice_1 is not 3, it means that the user still is in the submenu products - as soon as sub_choice_1 is 3, it means 
            # that the user wishes to exit the submenu
            while sub_choice_1 != "3":
                ## This submenu handles the adding of a new product
                if sub_choice_1 == "1":
                    ## Calling function to add a new product
                    self.add_product()
                    ## Calling function for the products submenu again (to loop)
                    self.products_menu_nav()
                    ## Asking for a new submenu input
                    sub_choice_1 = input("Select option: ")
                ## This submenu handles the editing of an existing product
                elif sub_choice_1 == "2":
                    ## Calling function to list and edit a products
                    self.list_products()
                    ## Calling a function for the products submenu again (to loop)
                    self.products_menu_nav()
                    ## Asking for a new submenu input
                    sub_choice_1 = input("Select option: ")
            ## Calling main menu again after loop for submenu ended
            self.main_menu_nav()
        ## Menu input 2 to display inventory information
        elif choice == "2":
            ## Loading the submenu for the inventory
            self.inventory_menu_nav()
            ## Asking for new input to navigate through the submenu
            sub_choice_2 = input("Select option: ")
            ## While sub_choice_2 is not 4, it means that the user still is in the submenu inventory - as soon as sub_choice_2 is 4, it means 
            # that the user wishes to exit the submenu
            while sub_choice_2 != "4":
                ## This submenu handles the adding of new inventory
                if sub_choice_2 == "1":
                    self.add_inventory()
                    ## Calling a function for the inventory submenu again (to loop)
                    self.inventory_menu_nav()
                    ## Asking for a new submenu input
                    sub_choice_2 = input("Select option: ")
                elif sub_choice_2 == "2":
                    self.remove_inventory()
                    ## Calling a function for the inventory submenu again (to loop)
                    self.inventory_menu_nav()
                    ## Asking for a new submenu input
                    sub_choice_2 = input("Select option: ")
                elif sub_choice_2 == "3":
                    self.list_inventory()
                    ## Calling a function for the inventory submenu again (to loop)
                    self.inventory_menu_nav()
                    ## Asking for a new submenu input
                    sub_choice_2 = input("Select option: ")
            ## Calling main menu again after loop for submenu ended
            self.main_menu_nav()
        ## Menu input 3 to display analytics information
        elif choice == "3":
             ## Loading submenu for users
            self.analytics_menu_nav()
            ## Asking for new input to navigate through the submenu
            sub_choice_3 = input("Select option: ")
            ## While sub_choice_3 is not 3, it means that the user still is in the submenu products - as soon as sub_choice_3 is 3, it means 
            # that the user wishes to exit the submenu
            while sub_choice_3 != "6":
                if sub_choice_3 == "1":
                    self.year_report_filtering()
                    self.analytics_menu_nav()
                    sub_choice_3 = input("Select option: ")
                elif sub_choice_3 == "2":
                    self.month_report_filtering()
                    self.analytics_menu_nav()
                    sub_choice_3 = input("Select option: ")
                elif sub_choice_3 == "3":
                    self.week_report_filtering()
                    self.analytics_menu_nav()
                    sub_choice_3 = input("Select option: ")
                elif sub_choice_3 == "4":
                    self.day_report_filtering()
                    self.analytics_menu_nav()
                    sub_choice_3 = input("Select option: ")
                elif sub_choice_3 == "5":
                    self.custom_report_filtering()
                    self.analytics_menu_nav()
                    sub_choice_3 = input("Select option: ")
        ## Menu input 4 to display user information
        elif choice == "4":
            ## Loading submenu for users
            self.users_menu_nav()
            ## Asking for new input to navigate through the submenu
            sub_choice_4 = input("Select option: ")
            ## While sub_choice_4 is not 3, it means that the user still is in the submenu products - as soon as sub_choice_1 is 3, it means 
            # that the user wishes to exit the submenu
            while sub_choice_4 != "3":
                if sub_choice_4 == "1":
                    self.add_user()
                    self.users_menu_nav()
                    sub_choice_4 = input("Select option: ")
                elif sub_choice_4 =="2":
                    self.list_users()
                    self.users_menu_nav()
                    sub_choice_4 = input("Select option: ")

            ## Calling main menu again after loop for submenu ended
            self.main_menu_nav()
        ## Menu input 5 to exit the app
        elif choice == "5":
            self.running = False

    ## Function to run the app while self.running is True
    def run(self):
        while self.running:
            pass


if __name__ == '__main__':
    myapp = Varasto()
    myapp.run()