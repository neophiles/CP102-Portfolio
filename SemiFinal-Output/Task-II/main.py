# Tagle, Marc Neil V.

from playlist_manager import Playlist_Manager
from user_menu import User_Menu
import utility

class Main_Menu:

    def __init__(self) -> None:
        pass

    def main(self) -> None:
        try:
            run = True
            m = None
            c = None

            print("SQL LOG-IN (enter blank to cancel)")
            while c is None:
                
                user = utility.get_input("Enter SQL Username: ")
                if user is None:
                    print("Log-in Cancelled.")
                    run = False
                    break
                    
                pswd = utility.get_input("Enter SQL Password: ")
                if pswd is None:
                    print("Log-in Cancelled.")
                    run = False
                    break

                m = Playlist_Manager()
                c = m.connect(user, pswd)

                if c:
                    print(f"Welcome, {user}!\n")
                    break
            
            while run:
                utility.title("PLAYLIST MANAGER")
                print("[1] Login (admin or user)")
                print("[2] Sign up")
                print("[0] Exit")

                while True:
                    choice = input("Enter operation: ")

                    if choice == "1":
                        utility.clear_screen()
                        user = m.user_login(c)
                        
                        if user is None:
                            break
                        else:
                            um = User_Menu()
                            um.main(m, c, user)
                        break

                    elif choice == "2":
                        utility.clear_screen()
                        m.sign_up(c)
                        break

                    elif choice == "0":
                        print()
                        utility.goodbye()
                        return None
                    
                    else:
                        print("Invalid option! Please try again.\n")

        except Exception as e:
            print(f"An unexpected error occurred: {e}.\n")
        
        finally:
            if c is not None:
                m.disconnect(c)

if __name__ == "__main__":
    menu = Main_Menu()
    menu.main()