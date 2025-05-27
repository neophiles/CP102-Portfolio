# Tagle, Marc Neil V.

from playlist_manager import Playlist_Manager
import utility

class Settings:

    def __init__(self) -> None:
        pass

    def main(self, m, c, user) -> bool | None:
        try:
            run = True
            
            while run:
                utility.title("SETTINGS")
                print("[1] Change Username")
                print("[2] Change Password")
                print("[3] Delete Account")
                print("[0] Back to User Menu")

                while True:
                    choice = input("Enter operation: ")

                    if choice == "1":
                        utility.clear_screen()
                        m.change_username(c, user)
                        break

                    elif choice == "2":
                        utility.clear_screen()
                        m.change_password(c, user)
                        break

                    elif choice == "3":
                        utility.clear_screen()
                        deleted = m.delete_account(c, user)
                        if deleted:
                            return False
                        break

                    elif choice == "0":
                        utility.clear_screen()
                        return True                  
                        
                    else:
                        print("Invalid option! Please try again.\n")

        except Exception as e:
            print(f"An unexpected error occurred: {e}.\n")