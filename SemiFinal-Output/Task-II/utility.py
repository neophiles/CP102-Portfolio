# Tagle, Marc Neil V.

import os

def title(title) -> None:
    print("=" * 10, title, "=" * 10)

def goodbye() -> None:
    print("Goodbye!")

def divider() -> None:
    print("=" * 40)

def clear_screen() -> None:
    os.system('cls')

def go_back() -> True:
    while True:
        go_back = input("Go back? [y]: ").lower()
        if go_back == 'y' or go_back == '':
            return True
        else:
            print("Invalid response! Please enter [y].")

def get_input(prompt) -> str:
        value = input(prompt)
        if value == "":
            return ""
        return value