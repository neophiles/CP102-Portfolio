# Tagle, Marc Neil V. (M001)

import csv
from tabulate import tabulate # Tabulate is a third-party module

class CSV_Manager:
    def __init__(self, file_name):
        self.file_name = file_name # Created object accepts a file name as argument.


    def view_csv(self):
        with open(self.file_name, 'r', newline = '') as csv_file:
            reader = csv.reader(csv_file)
            rows = list(reader) # Creates a list of all rows from the 'reader' iterator.

        if not rows: # Checks if file is empty.
            print("This file is empty.")
            return

        print(f"Processed {len(rows) - 1} lines (excluding headers):")
        if len(rows[0]) < 8: # Tabulates data if dataset if small.
            print(tabulate(rows, headers="firstrow", tablefmt="grid"))
        else:
            print("\n",", ".join(rows[0]),"\n")
            if len(rows[1:]) < 50: # If number of rows is less than 50, it shows all rows.
                for row in rows[1:]:
                    print("\t", ", ".join(row))
            else: # Shows a preview of the dataset if number of rows is greater than 50.
                for row in rows[1:6]:
                    print("\t", ", ".join(row))
                print("\t...") # Dataset is truncated.
                for row in rows[-5:]:
                    print("\t", ", ".join(row))


    def search_csv(self):
        with open(self.file_name, 'r', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = list(reader)
            field_names = reader.fieldnames
        
        if not rows or not field_names: # Checks if there are no rows or no columns.
            print("This file is empty.")
            return

        print("Columns:") # Shows all columns available.
        for field in field_names:
            print(f" - {field}")

        attempts = 3 # Limits number of tries for entering a valid column.
        # If all three attempts fail, the function exits and prompts the user for another operation.
        while attempts > 0:
            column = input("\nEnter column (or type 'exit' to cancel): ")
            if column.lower() == 'exit': # User can cancel searching.
                return
            if column not in field_names: 
                attempts -= 1 # Number of attempts is decremented upon entering an invalid column.
                print(f"Error: Column {column} not found! ({attempts} attempt(s) left)")
                continue
            else: # Entering a valid column will let user enter a search value.
                search_value = input("Search: ")
                # Filters the list 'rows' to find all rows where the value in the column matches
                # the given 'search_value' and stores them in 'rows_found'.
                rows_found = [row for row in rows if row[column] == search_value]
                
                if rows_found:
                    print(f"{len(rows_found)} row/s found:")
                    print("\n",", ".join(field_names),"\n") # Prints field names as header.
                    if len(rows_found[0]) < 8: # Tabulates data if dataset if small.
                        print(tabulate(rows_found, headers="keys", tablefmt="grid"))
                    else: # If dataset has too many columns, searched rows are printed normally line by line.
                        for row in rows_found:
                            print("\t", ", ".join(row.values()))
                else:
                    print("No match.") # Prints if no rows match.
                break


    def add_row(self):
        with open(self.file_name, 'r', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            field_names = reader.fieldnames

        if not field_names: # Checks if file is empty.
            print("This file is empty.")
            return

        new_row_list = []
        for field in field_names:
            row_value = input(f"Enter {field}: ")
            if row_value.lower() == 'exit': # User can cancel adding a row.
                return
            new_row_list.append(row_value)
        new_row_dict = {field: new_row_list[i] for i, field in enumerate(field_names)}

        with open(self.file_name, 'a', newline = '') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writerow(new_row_dict) # A new row is added with values of 'new_row_dict'
        print("New row added successfully!")


    def delete_row(self):
        with open(self.file_name, 'r', newline = '') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = list(reader)
            field_names = reader.fieldnames

        if not rows or not field_names: # Checks if there are no rows or no columns.
            print("This file is empty.")
            return

        print("Columns:") # Shows all columns available.
        for field in field_names:
            print(f" - {field}")

        attempts = 3 # Limits number of tries for entering a valid column.
        # If all three attempts fail, the function exits and prompts the user for another operation.
        while attempts > 0: 
            column = input("\nEnter column (or type 'exit' to cancel): ")
            if column.lower() == 'exit': # User can cancel deleting row/s.
                return
            if column not in field_names:
                attempts -= 1 # Number of attempts is decremented upon entering an invalid column.
                print(f"Error: Column {column} not found! ({attempts} attempt(s) left)")
                continue
            else: # Entering a valid column will let user enter a search value.
                delete_value = input("Delete: ")
                
                # Creates a list of all rows where the value in the specified 'column'
                # matches 'delete_value' (these rows will be deleted).
                rows_deleted = [row for row in rows if row[column] == delete_value]

                # Creates a list of all rows where the value in the specified 'column'
                # does NOT match 'delete_value' (these rows will remain in the dataset).
                rows_remain = [row for row in rows if row[column] != delete_value]      

                # Checks if any rows were deleted.
                if len(rows_remain) == len(rows) and not rows_deleted:
                    print("No row/s deleted.")
                else:
                    # Opens the CSV file to overwrite the content with 'rows_remain'.
                    with open(self.file_name, 'w', newline = '') as csv_file:
                        writer = csv.DictWriter(csv_file, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerows(rows_remain)

                    print(f"{len(rows_deleted)} row/s deleted successfully:") #  Shows deleted rows.
                    print("\n",", ".join(field_names),"\n") # Prints field names as header.
                    if len(rows_deleted[0]) < 8:
                        # Tabulates data if dataset if small.
                        print(tabulate(rows_deleted, headers="keys", tablefmt="grid"))
                    else:
                        # If dataset has too many columns, deleted rows are printed normally line by line.
                        for row in rows_deleted:
                            print("\t", ", ".join(row.values()))
                break

    def empty_out(self):        
        with open(self.file_name, 'r', newline = '') as csv_file:
            reader = csv.DictReader(csv_file)
            rows = list(reader)
            field_names = reader.fieldnames

        if not rows:
            print("This file is already empty or has no headers.")
            return
        
        while True:
            keep_header = input("Do you want to keep the headers? (y/n): ").lower()
            if keep_header in ['y','n']:
                break
            print("Invalid response! Enter 'y' or 'n'.")

        with open(self.file_name, 'w', newline = '') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)

            if keep_header == 'y':
                writer.writeheader()
                print(f"{self.file_name} has been emptied successfully, but headers were kept.")
            else:
                print(f"{self.file_name} has been completely emptied.")


    # Updates the file name to a new specified file and prints a confirmation message.
    def change_file(self, new_file):
        self.file_name = new_file
        print(f"File changed to {self.file_name}!")