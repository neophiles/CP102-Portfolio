# Tagle, Marc Neil V.

from playlist_manager import Playlist_Manager
import utility

class Playlist_Menu:

    def __init__(self) -> None:
        self.show_playlists = False
        self.show_songs = True

    def in_playlist(self, m, c, id, name, songs) -> None:
        try:
            run = True

            while run:
                songs = m._get_playlist_songs(c, name, id)
                
                if self.show_songs and songs:
                    m.show_playlist_songs(name, songs)
                    self.show_songs = False

                utility.title("NOW IN PLAYLIST")
                print("[1] Play Song")
                print("[2] Add Song")
                print("[3] Delete Song")
                print("[0] Back to My Playlists")

                while True:
                    choice = input("Enter operation: ")

                    if choice == "1":
                        utility.clear_screen()
                        m.show_playlist_songs(name, songs)
                        song_playing = m.play_song(name, songs)
                        if song_playing:
                            b = utility.go_back()
                            if b:
                                self.show_songs = True
                                utility.clear_screen()
                        break

                    elif choice == "2":
                        utility.clear_screen()
                        m.view_available_songs(c)
                        m.show_playlist_songs(name, songs)
                        m.add_playlist_song(c, id, name)
                        break

                    elif choice == "3":
                        utility.clear_screen()
                        if songs:
                            m.show_playlist_songs(name, songs)
                            m.delete_playlist_song(c, id, name, songs)
                        break

                    elif choice == "0":
                        self.show_playlists = True
                        self.show_songs = True
                        utility.clear_screen()
                        return None
                        
                    else:
                        print("Invalid option! Please try again.\n")

        except Exception as e:
            print(f"An unexpected error occurred: {e}.\n")


    def in_menu(self, m, c, user) -> None:
        try:
            run = True

            while run:
                if self.show_playlists:
                    m.view_playlists(c, user)
                    self.show_playlists = False

                utility.title("PLAYLIST MENU")
                print("[1] Open Playlist")
                print("[2] Change Playlist Name")
                print("[3] Delete Playlist")
                print("[0] Back to User Menu")

                while True:
                    choice = input("Enter operation: ")

                    if choice == "1":
                        utility.clear_screen()
                        m.view_playlists(c, user)
                        print("OPEN PLAYLIST (enter blank to cancel)")
                        playlist = m.get_playlist(c, "Open playlist cancelled.")
                        if playlist:
                            playlist_id = playlist[0]
                            playlist_name = playlist[1]
                            songs = m.open_playlist(c, playlist)
                            if songs:
                                utility.clear_screen()
                            self.in_playlist(m, c, playlist_id, playlist_name, songs)
                            break
                        else:
                            break

                    elif choice == "2":
                        utility.clear_screen()
                        m.view_playlists(c, user)
                        m.change_playlist_name(c)
                        break

                    elif choice == "3":
                        utility.clear_screen()
                        m.view_playlists(c, user)
                        print("DELETE PLAYLIST (enter blank to cancel)")
                        playlist = m.get_playlist(c, "Playlist deletion cancelled.")
                        if playlist:
                            m.delete_playlist(c, playlist)
                        break

                    elif choice == "0":
                        utility.clear_screen()
                        return None
                        
                    else:
                        print("Invalid option! Please try again.\n")

        except Exception as e:
            print(f"An unexpected error occurred: {e}.\n")