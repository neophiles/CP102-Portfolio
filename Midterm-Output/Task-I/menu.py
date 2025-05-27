# Tagle, Marc Neil V. (M001)

import os
from csv_file_manager import CSV_Manager

def get_valid_file():
    while True:
        file_name = input("Enter file name (with .csv extension): ").strip()
        if not file_name.endswith(".csv"):
            print("File is not CSV.") # Prints if file is not a CSV file.
            continue
        if not os.path.isfile(file_name):
            print(f"File not found.") # Prints if file is not found.
            continue
        return file_name # Returns the valid file name for use.
        
def separator():
    print("=" * 39)

def goodbye():
    print("Exiting CSV Manager. Goodbye!")


try:
    if __name__ == '__main__':
        print("=" * 13, "CSV MANAGER",  "=" * 13)
        file_name = get_valid_file() # Prompts user to enter a valid file name.
        manager = CSV_Manager(file_name) # Creates an object from 'CSV_Manager' class with the specified file name.

        proceed = True
        while proceed:
            separator()
            print("CSV Manager:")
            print("1 - View\n2 - Search\n3 - Add\n4 - Delete Row/s\n5 - Empty Out\n6 - Change File\n7 - Exit")
                
            try:
                operation = int(input("Enter operation: "))
            except ValueError: # Captures exception when user enters a non-numeric operation.
                print("Invalid operation!")
                continue
            
            separator()

            if operation == 1:
                manager.view_csv()

            elif operation == 2:
                manager.search_csv()

            elif operation == 3:
                manager.add_row()

            elif operation == 4:
                manager.delete_row()

            elif operation == 5:
                manager.empty_out()

            elif operation == 6:
                new_file = get_valid_file()
                manager.change_file(new_file)

            elif operation == 7:
                goodbye()
                break

            else: # Prints if user enters a invalid numeric operation.
                print("Invalid operation!")
                continue

            while True:
                cont = input("\nDo you want to perform another operation (y/n): ").lower()
                if cont in ['y','n']:
                    break
                print("Invalid response! Enter 'y' or 'n'.")

            if cont == 'n':
                proceed = False
                separator()
                goodbye()

except Exception as e: # Captures any unexpected errors to avoid crashes.
    print(f"An unexpected error occurred: {e}")