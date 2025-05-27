# Tagle, Marc Neil V.

from playlist_manager import Playlist_Manager
from playlist_menu import Playlist_Menu
from settings import Settings
import utility

class User_Menu:

    def __init__(self) -> None:
        pass

    def main(self, m, c, user) -> None:
        try:
            run = True
            
            while run:
                utility.title("USER MENU")
                print("[1] View Available Songs")
                print("[2] Add Song")
                print("[3] View My Playlists")
                print("[4] Create Playlist")
                print("[5] Settings")
                print("[0] Logout")

                while True:
                    choice = input("Enter operation: ")

                    if choice == "1":
                        utility.clear_screen()
                        m.view_available_songs(c)
                        b = utility.go_back()
                        if b:
                            utility.clear_screen()
                            break

                    elif choice == "2":
                        utility.clear_screen()
                        m.add_song(c)
                        break

                    elif choice == "3":
                        utility.clear_screen()
                        my_playlists = m.view_playlists(c, user)
                        if my_playlists:
                            pm = Playlist_Menu()
                            pm.in_menu(m, c, user)
                        break

                    elif choice == "4":
                        utility.clear_screen()
                        m.create_playlist(c, user)
                        break

                    elif choice == "5":
                        utility.clear_screen()
                        sm = Settings()
                        run = sm.main(m, c, user)
                        if run is False:
                            return None
                        else:
                            break

                    elif choice == "0":
                        utility.clear_screen()
                        is_logged_in = m.user_logout()
                        if is_logged_in == False:
                            return None
                        else:
                            print()
                            break                        
                        
                    else:
                        print("Invalid option! Please try again.\n")

        except Exception as e:
            print(f"An unexpected error occurred: {e}.\n")