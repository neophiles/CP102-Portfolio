# Tagle, Marc Neil V.

import mysql.connector
from mysql.connector import errorcode
from typing import Optional, Tuple, Any
import random as rd
import datetime
import utility

class Playlist_Manager:

    def __init__(self) -> None:
        self.logged_in = False

    
    @property
    def is_logged_in(self) -> bool:
        return self.logged_in


    @is_logged_in.setter
    def is_logged_in(self, value) -> None:
        self.logged_in = value
    

    def generate_id(self, prefix) -> str:
        rd_num = str(rd.randint(1, 999))

        if len(rd_num) == 3:
            rd_num = "0" + rd_num
        elif len(rd_num) == 2:
            rd_num = "00" + rd_num
        elif len(rd_num) == 1:
            rd_num = "000" + rd_num
        return "-".join([prefix.upper(), rd_num])


    def connect(self, user, pswd) -> Optional[mysql.connector.connection.MySQLConnection]:
        try:
            con = mysql.connector.connect(
                user=user,
                password=pswd,
                host='localhost',
                database='playlist'
            )
            print("Connection successful!")
            return con
        
        except mysql.connector.Error as err:

            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password.\n")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist.\n")
            else:
                print(err)
            return None

    
    def check_connection(self, con) -> None:
        if con is not None:
            try:

                if con.is_connected():
                    print("Connected to database!\n")
                else:
                    print("Connection has been lost!\n")

            except mysql.connector.Error as err:
                print(f"Error: {err}")

        else:
            print("No valid connection object to check.\n")

    
    def disconnect(self, con) -> None:
        con.close()
        print("Disconnection successful!")


    def get_playlist(self, con, cncl_msg=""):
        cursor = None
        try:
            cursor = con.cursor()

            playlist_id = utility.get_input("Enter Playlist ID: ")

            if playlist_id == "":
                print(f"{cncl_msg}\n")
                return None
            else:
                query1 = "SELECT * FROM Playlist_Details WHERE id = %s"
                cursor.execute(query1, (playlist_id,))
                playlist = cursor.fetchone()

            if playlist:
                return playlist
            else:
                return None 

        except mysql.connector.Error as err:
            print(err)
        
        finally:
            if cursor is not None:
                cursor.close()   


    def sign_up(self, con) -> None:
        cursor = None
        try:
            cursor = con.cursor()
            while True:
                
                print("SIGN UP (enter blank to cancel)")

                while True:
                    user_id = self.generate_id("USR")
                    query1 = "SELECT * FROM Users WHERE id = %s"
                    cursor.execute(query1, (user_id,))
                    existing_id = cursor.fetchone()

                    if existing_id is None:
                        break

                while True:
                    username = utility.get_input("Enter Username: ")

                    if username == "":
                        print("Sign up cancelled.\n")
                        return None
                    else:
                        query2 = "SELECT * FROM Users WHERE name = %s"
                        cursor.execute(query2, (username,))
                        existing_name = cursor.fetchone()
                        
                        if existing_name is None:
                            break
                        else:
                            print("Username already taken.\n")                        
                
                while True:
                    password = utility.get_input("Enter Password (max 10 characters): ")

                    if password == "":
                        print("Sign up cancelled.")
                        return None
                    else:
                        if len(password) > 10:
                            print("Invalid password. Maximum of 10 characters only.\n")
                        else:
                            break                        

                while True:
                    email = utility.get_input("Enter Email: ")

                    if email == "":
                        print("Sign up cancelled.\n")
                        return None
                    else:
                        if email.count("@") == 1 and email.index("@") > 0 and email.index("@") < len(email) - 1:
                            break
                        else:
                            print("Invalid email address.\n")
                        
                query = "INSERT INTO Users (id, name, password, email) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (user_id, username, password, email))
                con.commit()
                print(f"User '{username}' with email '{email}' added successfully.\n")
                return None

        except mysql.connector.Error as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()


    def user_login(self, con) -> Optional[Tuple[Any]]:
        cursor = None
        attempts = 3
        try:
            cursor = con.cursor()

            print("USER LOGIN (enter blank to cancel)")

            while attempts > 0:
                username = utility.get_input("Enter Username: ")
                
                if username == "":
                    print("Login cancelled.\n")
                    return None
                
                password = utility.get_input("Enter Password: ")
                if password == "":
                    print("Login cancelled.\n")
                    return None
                
                query = "SELECT * FROM Users WHERE name = %s AND password = %s"
                cursor.execute(query, (username, password))
                user = cursor.fetchone()

                if user:
                    print(f"Login successful! Welcome, {user[1]}!\n")
                    self.logged_in = True
                    return user
                else:
                    attempts -= 1
                    print(f"Invalid username or password. {attempts} attempts left.\n")

        except mysql.connector.Error as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()


    def user_logout(self) -> bool:
        print("USER LOGOUT (enter blank to cancel)")
        while True:
            logout = utility.get_input("Do you want to logout? [y/n]: ").lower()
            
            if logout == 'y':
                self.logged_in = False
                print("Logged out.\n")
                return self.logged_in
            elif logout == 'n':
                return self.logged_in
            else:
                print("Invalid response! Please enter [y/n].\n")


    def add_song(self, con) -> None:
        cursor = None
        try:
            cursor = con.cursor()
                
            print("ADD SONG TO DATABASE (enter blank to cancel)")

            while True:
                song_id = self.generate_id("SNG")
                query1 = "SELECT * FROM Songs WHERE id = %s"
                cursor.execute(query1, (song_id,))
                existing_id = cursor.fetchone()
                if existing_id is None:
                    break

            while True:
                song_title = utility.get_input("Enter Song Title: ")
                if song_title == "":
                    print("Add Song cancelled.\n")
                    return None

                artist = utility.get_input("Enter Artist: ")
                if artist == "":
                    print("Add Song cancelled.\n")
                    return None

                genre = utility.get_input("Enter Genre: ")
                if genre == "":
                    print("Add Song cancelled.\n")
                    return None

                query = "INSERT INTO Songs (id, title, artist, genre) VALUES (%s, %s, %s, %s)"

                cursor.execute(query, (song_id, song_title, artist, genre))
                con.commit()
                print(f"Added {song_title} by {artist}.\n")
                
                while True:
                    confirm = input("Do you want to add another song? [y/n]: ").lower()
                    if confirm == 'y':
                        print()
                        break
                    elif confirm == 'n':
                        print()
                        return None
                    else:
                        print("Invalid response! Please enter [y/n].\n")

        except mysql.connector.Error as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()


    def create_playlist(self, con, user) -> None:
        cursor = None
        try:
            cursor = con.cursor()
                
            print("CREATE PLAYLIST (enter blank to cancel)")

            while True:
                playlist_id = self.generate_id("LST")
                query1 = "SELECT * FROM Playlist_Details WHERE id = %s"
                cursor.execute(query1, (playlist_id,))
                existing_id = cursor.fetchone()
                if existing_id is None:
                    break
            
            while True:
                playlist_name = utility.get_input("Enter Playlist Name: ")

                if playlist_name == "":
                    print("Playlist creation cancelled.\n")
                    return None
                
                query1 = "SELECT id FROM Playlist_Details WHERE name = %s"
                cursor.execute(query1, (playlist_name,))
                existing_playlist = cursor.fetchone()

                if existing_playlist:
                    print("A playlist with this name already exists.\n")
                else:
                    user_id = user[0]

                    query2 = "INSERT INTO Playlist_Details (id, name, user_id) VALUES (%s, %s, %s)"
                    cursor.execute(query2, (playlist_id, playlist_name, user_id))
                    con.commit()
                    print(f"Playlist '{playlist_name}' created.\n")
                    
                    while True:
                        confirm = input("Do you want to create another playlist? [y/n]: ").lower()
                        if confirm == 'y':
                            print()
                            break
                        elif confirm == 'n':
                            print()
                            return None
                        else:
                            print("Invalid response! Please enter [y/n].\n")

        except mysql.connector.Error as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()


    def add_playlist_song(self, con, playlist_id, playlist_name) -> None:
        cursor = None
        try:
            cursor = con.cursor()
                
            print("ADD SONG TO PLAYLIST (enter blank to cancel)")
            while True:
                song_id = utility.get_input("Enter Song ID: ")
                if song_id == "":
                    print("Add song cancelled.")
                    return None

                query1 = "SELECT * FROM Songs WHERE id = %s"
                cursor.execute(query1, (song_id,))
                song_to_add = cursor.fetchone()

                if song_to_add is None:
                    print(f"Song ID '{song_id}' does not exist. Please try again.\n")
                    continue

                query2 = "INSERT INTO Playlist_Songs (playlist_id, song_id) VALUES (%s, %s)"
                cursor.execute(query2, (playlist_id, song_id))
                con.commit()

                added_song_name = song_to_add[1]
                print(f"Successfully added {added_song_name} to {playlist_name}.\n")
                
                while True:
                    confirm = input("Do you want to add another song? [y/n]: ").lower()
                    if confirm == 'y':
                        print()
                        break
                    elif confirm == 'n':
                        print()
                        return None
                    else:
                        print("Invalid response! Please enter [y/n].\n")

        except mysql.connector.Error as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()


    def change_username(self, con, user) -> None:
        cursor = None
        try:
            cursor = con.cursor()
            
            print("CHANGE USERNAME (enter blank to cancel)")

            if user is not None:

                while True:
                    new_username = utility.get_input("Enter New Username: ")

                    if new_username == "":
                        print("Change username cancelled.\n")
                        return None
                    
                    elif new_username == user[1]:
                        print("You cannot set the same username as before.\n")

                    else:
                        break
                
                while True:
                    confirm = input("Confirm new username? [y/n]: ").lower()
                    if confirm == 'y':
                        break
                    elif confirm == 'n':
                        print("Change username cancelled.\n")
                        return None
                    else:
                        print("Invalid response! Please enter [y/n].\n")

                query = "UPDATE Users SET name = %s WHERE name = %s AND password = %s"
                cursor.execute(query, (new_username, user[1], user[2]))
                
                con.commit()
                print(f"Username Updated! Hello, {new_username}!\n")
                return None

            else:
                print("User not found.\n")
                return None

        except mysql.connector.Error as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()


    def change_password(self, con, user) -> None:
        cursor = None
        attempts = 3
        try:
            cursor = con.cursor()
                
            print("CHANGE PASSWORD (enter blank to cancel)")

            if user is not None:

                while attempts > 0:
                    old_pass = utility.get_input("Enter Old Password: ")

                    if old_pass == "":
                        print("Change password cancelled.\n")
                        return None
                    
                    elif old_pass == user[2]:
                        while True:
                            new_pass = utility.get_input("Enter New Password: ")
                            if new_pass == "":
                                print("Change password cancelled.\n")
                                return None
                            elif new_pass == old_pass:
                                print("You cannot set the same password as before.\n")
                            else:
                                break
                        
                    else:
                        attempts -= 1
                        print(f"\nIncorrect password! {attempts} attempts left.\n")

                    while True:
                        confirm = input("Confirm new password? [y/n]: ").lower()
                        if confirm == 'y':
                            break
                        elif confirm == 'n':
                            print("Change password cancelled.\n")
                            return None
                        else:
                            print("Invalid response! Please enter [y/n].\n")

                    query = "UPDATE Users SET password = %s WHERE name = %s AND password = %s"
                    cursor.execute(query, (new_pass, user[1], user[2]))
                    con.commit()
                    print("Password Updated!\n")
                    return None

            else:
                print("User not found.\n")
                return

        except mysql.connector.Error as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()
    
    
    def change_playlist_name(self, con) -> None:
        cursor = None
        try:
            cursor = con.cursor()
                
            print("CHANGE PLAYLIST NAME (enter blank to cancel)")

            while True:
                playlist_id = utility.get_input("Enter Playlist ID: ")
                if playlist_id == "":
                    print("Change playlist name cancelled.\n")
                    return None
                
                else:
                    query1 = "SELECT name FROM Playlist_Details WHERE id = %s"
                    cursor.execute(query1, (playlist_id,))
                    playlist = cursor.fetchone()

                if not playlist:
                    print("Playlist not found.\n")
                else:
                    current_name = playlist[0]
                    break

            while True:
                new_name = utility.get_input("Enter New Playlist Name: ")
                if new_name == "":
                    print("Change playlist name cancelled.\n")
                    return None
                elif new_name == current_name:
                    print("You cannot set the same name as before.\n")
                else:
                    break          

            while True:
                confirm = input("Confirm new playlist name? [y/n]: ").lower()
                if confirm == 'y':
                    break
                elif confirm == 'n':
                    print("Change playlist name cancelled.\n")
                    return None
                else:
                    print("Invalid response! Please enter [y/n].\n")

            query = "UPDATE Playlist_Details SET name = %s WHERE id = %s"
            cursor.execute(query, (new_name, playlist_id))
            con.commit()
            print(f"{current_name} changed to {new_name}.\n")
            return None

        except mysql.connector.Error as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()


    def delete_playlist(self, con, playlist) -> None:
        cursor = None
        try:
            cursor = con.cursor()

            if playlist is None:
                print("Playlist not found.\n")
                return None
            else:
                playlist_id = playlist[0]
                playlist_name = playlist[1]
            
            while True:
                delete = utility.get_input(f"Do you want to delete {playlist_name}? [y/n]: ").lower()
                                
                if delete == 'y':
                    query = "DELETE FROM Playlist_Details WHERE id = %s"

                    cursor.execute(query, (playlist_id,))
                    con.commit()
                    print(f"{playlist_name} successfully deleted.\n")
                    return None
                
                elif delete == 'n':
                    return None
                
                else:
                    print("Invalid response! Please enter [y/n].\n")
            

        except mysql.connector.Error as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()


    def delete_playlist_song(self, con, playlist_id, playlist_name, songs) -> None:
        cursor = None
        try:
            cursor = con.cursor()
                
            print("DELETE SONG IN PLAYLIST (enter blank to cancel)")

            while True:                    
                song_id = utility.get_input("Enter Song ID: ")

                if song_id == "":
                    print("Song deletion cancelled.\n")
                    return None
                
                query1 = "SELECT * FROM Songs WHERE id = %s"
                cursor.execute(query1, (song_id,))
                song = cursor.fetchone()

                if song is None:
                    print(f"Song ID '{song_id}' does not exist.\n")
                    continue
                    
                song_name = song[1]

                query2 = "SELECT * FROM Playlist_Songs WHERE playlist_id = %s AND song_id = %s"
                cursor.execute(query2, (playlist_id, song_id))
                in_playlist = cursor.fetchone()
                if in_playlist is None:
                    print(f"{song_name} is not in {playlist_name}.\n")
                    continue
        
                while True:
                    delete = utility.get_input(f"Do you want to remove {song_name}? [y/n]: ").lower()
                                    
                    if delete == 'y':
                        query4 = "DELETE FROM Playlist_Songs WHERE playlist_id = %s AND song_id = %s"
                        cursor.execute(query4, (playlist_id, song_id))
                        con.commit()
                        print(f"Successfully removed {song_name} from {playlist_name}.\n")
                        break
                    
                    elif delete == 'n':
                        return None
                    
                    else:
                        print("Invalid response! Please enter [y/n].\n")

                while True:
                    confirm = input("Do you want to remove another song? [y/n]: ").lower()
                    if confirm == 'y':
                        print()
                        break
                    elif confirm == 'n':
                        print()
                        return None
                    else:
                        print("Invalid response! Please enter [y/n].\n")

        except mysql.connector.Error as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()


    def delete_account(self, con, user) -> None:
        cursor = None
        attempts = 3
        try:
            cursor = con.cursor()

            print("DELETE ACCOUNT (enter blank to cancel)")

            if user is not None:
                while attempts > 0:
                    password = utility.get_input("Enter Password: ")

                    if password == "":
                        print("Account deletion cancelled.\n")
                        return None
                    
                    elif password == user[2]:
                        while True:
                            delete = utility.get_input("Do you want to delete your account? [y/n]: ").lower()
                            
                            if delete == "":
                                print("Account deletion cancelled.\n")
                                return None
                            
                            elif delete == 'y':
                                query = "DELETE FROM Users Where name = %s AND password = %s"

                                cursor.execute(query, (user[1], user[2]))
                                con.commit()
                                self.logged_in = False
                                print("Account successfully deleted. Goodbye!\n")
                                return True
                            
                            elif delete== 'n':
                                return None
                            
                            else:
                                print("Invalid response! Please enter [y/n].\n")
                    
                    else:
                        attempts -= 1
                        print(f"\nIncorrect password! {attempts} attempts left.")
            
            else:
                print("User not found.\n")
                return None

        except mysql.connector.Error as err:
            print(err)

        finally:
            if cursor is not None:
                cursor.close()


    def view_available_songs(self, con) -> None:
        cursor = None
        try:
            cursor = con.cursor()
            query = "SELECT * FROM Songs"
            cursor.execute(query)
            songs = cursor.fetchall()

            if songs:
                print("AVAILABLE SONGS:")
            else:
                print("No Available Songs.\n")

            for s in songs:
                print(s)
            print()
            return None

        except mysql.connector.Error as err:
            print(err)
        
        finally:
            if cursor is not None:
                cursor.close()


    def view_playlists(self, con, user) -> list[tuple[str, ...]] | None:
        cursor = None
        try:
            cursor = con.cursor()
            user_id = user[0]
            query = "SELECT * FROM Playlist_Details WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            raw_playlists = cursor.fetchall()

            if raw_playlists:
                print("MY PLAYLISTS:")
            else:
                print("You have no playlists.\n")
                return None

            final_playlists = []
            for i, p in enumerate(raw_playlists, start=1):
                p_id = p[0]
                p_name = p[1]
                p_date = p[3]
                readable_date = p_date.strftime("%B %d, %Y - %I:%M %p")
                p_details = (p_id, p_name, readable_date)
                final_playlists.append(p_details)
                print(f"{i}. {p_details}")
            print()
            
            return final_playlists

        except mysql.connector.Error as err:
            print(err)
        
        finally:
            if cursor is not None:
                cursor.close()


    def open_playlist(self, con, playlist) -> list[tuple[str, ...]] | None:
        cursor = None
        try:
            cursor = con.cursor()

            if playlist is None:
                print("Playlist not found.\n")
                return None
            else:
                playlist_id = playlist[0]
                playlist_name = playlist[1]

            query1 = "SELECT song_id FROM Playlist_Songs WHERE playlist_id = %s"
            cursor.execute(query1, (playlist_id,))
            song_id_results = cursor.fetchall()

            if not song_id_results:
                #print(f"\n{playlist_name} has no songs.\n")
                return None

            song_ids = [s[0] for s in song_id_results]

            format_strings = ','.join(['%s'] * len(song_ids)) 
            query2 = f"SELECT * FROM Songs WHERE id IN ({format_strings})"
            cursor.execute(query2, song_ids)
            songs = cursor.fetchall()

            if songs:
                print(songs)
                return songs
            else:
                #print(f"\n{playlist_name} has no songs.\n")
                return None
            

        except mysql.connector.Error as err:
            print(err)
        
        finally:
            if cursor is not None:
                cursor.close()


    def show_playlist_songs(self, name, songs) -> None:
        utility.title(name.upper())
        for i, s in enumerate(songs, start=1):
            print(f"{i}. {s}")
        print()
        return None
    

    def _get_playlist_songs(self, con, playlist_name, playlist_id) -> list[tuple[str, ...]]:
        cursor = None
        try:
            cursor = con.cursor()

            query1 = "SELECT song_id FROM Playlist_Songs WHERE playlist_id = %s"
            cursor.execute(query1, (playlist_id,))
            song_id_results = cursor.fetchall()

            if not song_id_results:
                print(f"{playlist_name} has no songs.\n")
                return []

            song_ids = [s[0] for s in song_id_results]
            format_strings = ','.join(['%s'] * len(song_ids)) 
            query2 = f"SELECT * FROM Songs WHERE id IN ({format_strings})"
            cursor.execute(query2, song_ids)
            return cursor.fetchall()

        except mysql.connector.Error as err:
            print(err)
            return []

        finally:
            if cursor is not None:
                cursor.close()


    def play_song(self, playlist_name, songs) -> tuple | None:
        print("PLAY SONG (enter blank to cancel)")
        
        song_ids = [song[0] for song in songs]

        while True:
            choice = utility.get_input("Enter ID of the song to play: ")

            if choice == "":
                print("Play song cancelled.\n")
                return None
            
            if choice in song_ids:
                song_playing = next(song for song in songs if song[0] == choice)
                print(f"\nNow playing: {song_playing[1]} by {song_playing[2]}.\n")
                return song_playing
            else:
                print(f"{choice} not found in {playlist_name}.\n")