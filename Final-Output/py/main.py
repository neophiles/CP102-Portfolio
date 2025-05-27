# Tagle, Marc Neil V.

from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox, QLabel, QFrame
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt, QDate
from PyQt6.uic import loadUi
import sys
from datetime import datetime
from db import get_people, insert_person, edit_person, delete_person, get_gifts, insert_gift, edit_gift, delete_gift, get_people_with_reminders
from reminders import days_until_birthday, group_by_upcoming, notify_upcoming_birthdays
    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ui/main.ui", self)
        self.setFixedSize(self.size())

        self.managePeopleButton.clicked.connect(self.open_manage_people_window)
        self.remindersButton.clicked.connect(self.open_reminders_window)
        self.giftsButton.clicked.connect(self.open_gift_ideas_window)
        self.exitButton.clicked.connect(self.quit_program)

    def open_manage_people_window(self):
        self.manage_people_window = ManagePeopleWindow(self)
        self.manage_people_window.show()
        self.hide()

    def open_reminders_window(self):
        self.reminders_window = RemindersWindow(self)
        self.reminders_window.show()
        self.hide()

    def open_gift_ideas_window(self):
        self.gift_ideas_window = GiftIdeasWindow(self)
        self.gift_ideas_window.show()
        self.hide()

    def quit_program(self):
        QApplication.quit()
        print("Program closed.")


class ManagePeopleWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        loadUi("ui/manage_people.ui", self)
        self.setFixedSize(self.size())
        self.main_window = main_window

        self.load_people()
        self.addPersonButton.clicked.connect(self.open_add_person_window)
        self.editPersonButton.clicked.connect(self.open_edit_person_window)
        self.deletePersonButton.clicked.connect(self.delete_person)
        self.searchLineEdit.textChanged.connect(self.filter_people)
        self.backButton.clicked.connect(self.go_back)

    def load_people(self):
        self.people_data = get_people()

        if self.people_data is None:
            QMessageBox.critical(self, "Error", "Failed to load people from the database.")
            return

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Birth Date", "Email", "Phone", "Notes"])

        for row in self.people_data:
            items = [QStandardItem(str(field)) for field in row]
            model.appendRow(items)

        self.peopleTableView.setModel(model)
        self.peopleTableView.setColumnHidden(0, True)
        self.peopleTableView.resizeColumnsToContents()       

    def open_add_person_window(self):
        self.add_person_window = AddPersonWindow(callback=self.load_people)
        self.add_person_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.add_person_window.show()

    def open_edit_person_window(self):
        selected_person = self.peopleTableView.selectedIndexes()
        if not selected_person:
            QMessageBox.warning(self, "Selection Error", "Please select a person to edit.")
            return
    
        person_id = self.peopleTableView.model().item(selected_person[0].row(), 0).text()
        first_name = self.peopleTableView.model().item(selected_person[0].row(), 1).text()
        last_name = self.peopleTableView.model().item(selected_person[0].row(), 2).text()
        birth_date = self.peopleTableView.model().item(selected_person[0].row(), 3).text()
        email = self.peopleTableView.model().item(selected_person[0].row(), 4).text()
        phone = self.peopleTableView.model().item(selected_person[0].row(), 5).text()
        notes = self.peopleTableView.model().item(selected_person[0].row(), 6).text()

        self.edit_person_window = EditPersonWindow(person_id, first_name, last_name, birth_date, email, phone, notes, callback=self.load_people)
        self.edit_person_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.edit_person_window.show()

    def delete_person(self):
        selected_person = self.peopleTableView.selectedIndexes()
        if not selected_person:
            QMessageBox.warning(self, "Selection Error", "Please select a person to delete.")
            return

        row = selected_person[0].row()
        person_id = self.peopleTableView.model().item(row, 0).text()
        first_name = self.peopleTableView.model().item(row, 1).text()
        last_name = self.peopleTableView.model().item(row, 2).text()

        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete {first_name} {last_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            if delete_person(person_id):
                QMessageBox.information(self, "Deleted", "Person deleted successfully.")
                print("Person deleted successfully.")
                self.load_people()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete person.")
                print("Failed to delete person.")

    def filter_people(self, text):
        filtered = []
        text = text.lower()

        for row in self.people_data:
            if any(text in str(field).lower() for field in row[1:]):
                filtered.append(row)

        self.update_people_table(filtered)

    def update_people_table(self, data):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["ID", "First Name", "Last Name", "Birth Date", "Email", "Phone", "Notes"])

        for row in data:
            items = [QStandardItem(str(field)) for field in row]
            model.appendRow(items)

        self.peopleTableView.setModel(model)
        self.peopleTableView.setColumnHidden(0, True)
        self.peopleTableView.resizeColumnsToContents()

    def go_back(self):
        self.main_window.show()
        self.close()


class AddPersonWindow(QWidget):
    def __init__(self, callback=None):
        super().__init__()
        loadUi("ui/add_person.ui", self)
        self.setFixedSize(self.size())
        
        self.callback = callback
        
        self.addPersonSaveButton.clicked.connect(self.save_person)
        self.addPersonCancelButton.clicked.connect(self.cancel)

    def save_person(self):
        first_name = self.addFirstName.text()
        last_name = self.addLastName.text()
        email = self.addEmail.text()
        phone = self.addNumber.text()
        birth_date = self.addBirthDate.date().toString("yyyy-MM-dd")
        notes = self.addPersonNotes.toPlainText()

        if not first_name or not last_name:
            QMessageBox.warning(self, "Input Error", "First name and last name cannot be empty.")
            return

        print("Saving person:", first_name, last_name, birth_date, email, phone, notes)

        success = insert_person(first_name, last_name, birth_date, email, phone, notes)

        if success:
            QMessageBox.information(self, "Deleted", "Person added successfully.")
            print("Person added successfully.")
            if self.callback:
                self.callback()         
            self.close()   
        else:
            QMessageBox.warning(self, "Error", "Failed to add person.")
            print("Failed to add person.")

    def cancel(self):
        self.close()
    

class EditPersonWindow(QWidget):
    def __init__(self, person_id, first_name, last_name, birth_date, email, phone, notes, callback=None):
        super().__init__()
        loadUi("ui/edit_person.ui", self)
        self.setFixedSize(self.size())

        self.person_id = person_id
        self.callback = callback

        self.editFirstName.setText(first_name)
        self.editLastName.setText(last_name)
        self.editBirthDate.setDate(QDate.fromString(birth_date, "yyyy-MM-dd"))
        self.editEmail.setText(email)
        self.editNumber.setText(phone)
        self.editPersonNotes.setPlainText(notes)

        self.editPersonSaveButton.clicked.connect(self.save_person)
        self.editPersonCancelButton.clicked.connect(self.cancel)

    def save_person(self):
        first_name = self.editFirstName.text()
        last_name = self.editLastName.text()
        email = self.editEmail.text()
        phone = self.editNumber.text()
        birth_date = self.editBirthDate.date().toString("yyyy-MM-dd")
        notes = self.editPersonNotes.toPlainText()

        success = edit_person(first_name, last_name, birth_date, email, phone, notes, self.person_id)

        if success:
            QMessageBox.information(self, "Success", "Person information updated successfully.")
            print("Information updated successfully!")
            if self.callback:
                self.callback()         
            self.close()   
        else:
            QMessageBox.warning(self, "Error", "Failed to update information.")
            print("Failed to update information.")

    def cancel(self):
        self.close()


class GiftIdeasWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        loadUi("ui/gift_ideas.ui", self)
        self.setFixedSize(self.size())
        self.main_window = main_window

        self.load_gifts()
        self.addGiftButton.clicked.connect(self.open_add_gift_window)
        self.editGiftButton.clicked.connect(self.open_edit_gift_window)
        self.deleteGiftButton.clicked.connect(self.delete_gift)
        self.searchLineEdit.textChanged.connect(self.filter_gifts)
        self.backButton.clicked.connect(self.go_back)

    def load_gifts(self):
        self.gifts_data = get_gifts()

        if self.gifts_data is False:
            QMessageBox.warning(self, "Load Error", "Could not load gifts data.")
            self.close()
            return

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["ID", "Person", "Gift Name", "Description", "Place", "Link", "Price", "Notes"])

        for row in self.gifts_data:
            items = [QStandardItem(str(field)) for field in row]
            model.appendRow(items)

        self.giftsTableView.setModel(model)
        self.giftsTableView.setColumnHidden(0, True)
        self.giftsTableView.resizeColumnsToContents()       

    def open_add_gift_window(self):
        people_data = get_people()

        if people_data is False:
            QMessageBox.warning(self, "Load Error", "Could not load people data.")
            return

        if not people_data:
            QMessageBox.warning(self, "No People", "You have no people in the database.")
            return

        self.add_gifts_window = AddGiftsWindow(people_data=people_data, callback=self.load_gifts)
        self.add_gifts_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.add_gifts_window.show()

    def open_edit_gift_window(self):

        if not self.gifts_data:
            QMessageBox.warning(self, "No Gifts", "You have no gifts in the database.")
            return

        selected_gift = self.giftsTableView.selectedIndexes()
        if not selected_gift:
            QMessageBox.warning(self, "Selection Error", "Please select a gift to edit.")
            return
    
        gift_id = self.giftsTableView.model().item(selected_gift[0].row(), 0).text()
        person = self.giftsTableView.model().item(selected_gift[0].row(), 1).text()
        gift_name = self.giftsTableView.model().item(selected_gift[0].row(), 2).text()
        description = self.giftsTableView.model().item(selected_gift[0].row(), 3).text()
        place = self.giftsTableView.model().item(selected_gift[0].row(), 4).text()
        link = self.giftsTableView.model().item(selected_gift[0].row(), 5).text()
        price = self.giftsTableView.model().item(selected_gift[0].row(), 6).text()
        notes = self.giftsTableView.model().item(selected_gift[0].row(), 7).text()

        self.edit_gifts_window = EditGiftsWindow(gift_id, person, gift_name, description, place, link, price, notes, callback=self.load_gifts)
        self.edit_gifts_window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.edit_gifts_window.show()

    def delete_gift(self):

        if not self.gifts_data:
            QMessageBox.warning(self, "No Gifts", "You have no gifts in the database.")
            return
        
        selected_gift = self.giftsTableView.selectedIndexes()
        if not selected_gift:
            QMessageBox.warning(self, "Selection Error", "Please select a gift to delete.")
            return

        row = selected_gift[0].row()
        gift_id = self.giftsTableView.model().item(row, 0).text()
        person = self.giftsTableView.model().item(row, 1).text()
        gift_name = self.giftsTableView.model().item(row, 2).text()

        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the gift '{gift_name}' for {person}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            if delete_gift(gift_id):
                QMessageBox.information(self, "Deleted", "Gift deleted successfully.")
                print("Gift deleted successfully.")
                self.load_gifts()
            else:
                QMessageBox.warning(self, "Error", "Failed to delete gift.")
                print("Failed to delete gift.")

    def filter_gifts(self, text):
        filtered = []
        text = text.lower()

        for row in self.gifts_data:
            if any(text in str(field).lower() for field in row[1:]):
                filtered.append(row)

        self.update_gifts_table(filtered)

    def update_gifts_table(self, data):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["ID", "Person", "Gift Name", "Description", "Place", "Link", "Price", "Notes"])

        for row in data:
            items = [QStandardItem(str(field)) for field in row]
            model.appendRow(items)

        self.giftsTableView.setModel(model)
        self.giftsTableView.setColumnHidden(0, True)
        self.giftsTableView.resizeColumnsToContents()

    def go_back(self):
        self.main_window.show()
        self.close()


class AddGiftsWindow(QWidget):
    def __init__(self, people_data, callback=None):
        super().__init__()
        loadUi("ui/add_gift.ui", self)
        self.setFixedSize(self.size())

        self.people_data = people_data
        self.callback = callback

        self.populate_people_combobox()
        self.addGiftSaveButton.clicked.connect(self.save_gift)
        self.addGiftCancelButton.clicked.connect(self.cancel)

    def populate_people_combobox(self):
        self.addPersonComboBox.clear()
        for person in self.people_data:
            person_id, first_name, last_name, *_ = person
            full_name = f"{first_name} {last_name}"
            self.addPersonComboBox.addItem(full_name, userData=person_id)

    def save_gift(self):
        person_id = self.addPersonComboBox.currentData()
        gift_name = self.addGiftName.text().strip()
        description = self.addDescription.toPlainText().strip()
        place = self.addPlace.text().strip()
        link = self.addLink.text().strip()
        price = self.addPrice.text().strip()
        notes = self.addGiftNotes.toPlainText().strip()

        if not person_id or not gift_name:
            QMessageBox.warning(self, "Input Error", "Person and gift name cannot be empty.")
            return

        if price != "":
            try:
                price = float(price)
                if price < 0:
                    raise ValueError("Price cannot be negative.")
                if price > 1_000_000:
                    raise ValueError("Price is unrealistically high.")
            except ValueError as ve:
                QMessageBox.warning(self, "Invalid Price", f"Please enter a valid price.\n\n{ve}")
                return

        success = insert_gift(person_id, gift_name, description, place, link, price, notes)

        if success:
            QMessageBox.information(self, "Success", "Gift added successfully.")
            print("Gift added successfully.")
            if self.callback:
                self.callback()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Failed to add gift.")
            print("Failed to add gift.")

    def cancel(self):
        self.close()


class EditGiftsWindow(QWidget):
    def __init__(self, gift_id, person, gift_name, description, place, link, price, notes, callback=None):
        super().__init__()
        loadUi("ui/edit_gift.ui", self)
        self.setFixedSize(self.size())

        self.gift_id = gift_id
        self.callback = callback

        self.populate_people_combobox(person)

        self.editGiftName.setText(gift_name)
        self.editDescription.setPlainText(description)
        self.editPlace.setText(place)
        self.editLink.setText(link)
        self.editPrice.setText(price)
        self.editGiftNotes.setPlainText(notes)

        self.editGiftSaveButton.clicked.connect(self.save_gift)
        self.editGiftCancelButton.clicked.connect(self.cancel)

    def populate_people_combobox(self, current_person_name):
        self.people_data = get_people()
        if self.people_data is None:
            QMessageBox.warning(self, "No People", "You have no people in the database.")
            return
        
        self.editPersonComboBox.clear()

        selected_index = 0
        for i, person in enumerate(self.people_data):
            person_id, first_name, last_name, *_ = person
            full_name = f"{first_name} {last_name}"
            self.editPersonComboBox.addItem(full_name, userData=person_id)

            if full_name == current_person_name:
                selected_index = i
        
        self.editPersonComboBox.setCurrentIndex(selected_index)

    def save_gift(self):
        person_id = self.editPersonComboBox.currentData()
        gift_name = self.editGiftName.text().strip()
        description = self.editDescription.toPlainText().strip()
        place = self.editPlace.text().strip()
        link = self.editLink.text().strip()
        price = self.editPrice.text().strip()
        notes = self.editGiftNotes.toPlainText().strip()

        if not person_id or not gift_name:
            QMessageBox.warning(self, "Input Error", "Person and gift name cannot be empty.")
            return

        try:
            price = float(price)
            if price < 0:
                raise ValueError("Price cannot be negative.")
            if price > 1_000_000:
                raise ValueError("Price is unrealistically high.")
        except ValueError as ve:
            QMessageBox.warning(self, "Invalid Price", f"Please enter a valid price.\n\n{ve}")
            return
        
        success = edit_gift(person_id, gift_name, description, place, link, price, notes, self.gift_id)

        if success:
            QMessageBox.information(self, "Success", "Gift updated successfully.")
            print("Gift updated successfully.")
            if self.callback:
                self.callback()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Failed to update gift.")
            print("Failed to update gift.")

    def cancel(self):
        self.close()


class RemindersWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        loadUi("ui/reminders.ui", self)
        self.setFixedSize(self.size())
        self.main_window = main_window

        self.backButton.clicked.connect(self.go_back)
        self.load_reminders()

    def load_reminders(self):
        people = get_people_with_reminders()
        if not people:
            QMessageBox.warning(self, "No Data", "No reminder-enabled people found.")
            return

        grouped = group_by_upcoming(people)

        self.populate_group(self.todayFrame, grouped["Today"])
        self.populate_group(self.thisWeekFrame, grouped["This Week"])
        self.populate_group(self.nextWeekFrame, grouped["Next Week"])
        self.populate_group(self.upcomingFrame, grouped["Upcoming"])

        notify_upcoming_birthdays(grouped)

    def create_vline(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line

    def populate_group(self, frame, group_data):
        layout = frame.layout()
        self.clear_layout(layout)

        for row, (person, _) in enumerate(group_data):
            name = f"{person['first_name']} {person['last_name']}"
            days_left = days_until_birthday(person['birth_date'])
            person_id = person['person_id']

            birth_date = datetime.strptime(person["birth_date"], "%Y-%m-%d")
            formatted_date = birth_date.strftime("%B %#d")

            name_label = QLabel(name)
            date_label = QLabel(formatted_date)
            days_left_label = QLabel(f"{days_left} days left")

            layout.addWidget(name_label, row, 0)
            layout.addWidget(self.create_vline(), row, 1)
            layout.addWidget(date_label, row, 2)
            layout.addWidget(self.create_vline(), row, 3)
            layout.addWidget(days_left_label, row, 4)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def go_back(self):
        self.main_window.show()
        self.close()


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        ui = MainWindow()
        ui.show()
        app.exec()
    except Exception as e:
        print("Fatal error:", e)