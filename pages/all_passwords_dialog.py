from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QPushButton, QWidget
from PySide6.QtCore import Qt
from security import decrypt_identifier, decrypt_password
from collections import defaultdict
import json
import os


class AllPasswordsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Password Manager")
        self.setModal(True)  # Make it modal

        # Layout for the all passwords page
        layout = QVBoxLayout()

        # Title label for the page
        title_label = QLabel("All Passwords", self)
        title_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #FFFF00;")
        layout.addWidget(title_label)

        # Create a widget to hold the list of all passwords
        all_passwords_widget = self.build_all_passwords_ui()

        # Set up the scroll area to hold the password list
        self.setup_scroll_area(layout, all_passwords_widget)

        self.setLayout(layout)

        # Set the dialog size to match the main window
        if parent is not None:
            self.resize(parent.size())

    def setup_scroll_area(self, layout, widget):
        """Set up the scroll area"""
        scroll_area = QScrollArea(self)
        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

    def build_all_passwords_ui(self):
        """Build the list of all usernames and their passwords."""
        passwords_widget = QWidget(self)
        passwords_layout = QVBoxLayout(passwords_widget)

        # Load the identifiers, passwords and IDs from the JSON file
        file_path = "passwords.json"
        if os.path.exists(file_path) and os.stat(file_path).st_size > 0:
            with open(file_path, 'r') as file:
                data = json.load(file)
        else:
            data = []

        grouped_passwords = defaultdict(list)

        for entry in data:
            # Decrypt the identifier and password
            decrypted_identifier = decrypt_identifier(entry['identifier'])
            decrypted_password = decrypt_password(entry['password'])

            # Group all passwords and IDs under the same identifier
            grouped_passwords[decrypted_identifier].append(
                {"id": entry['id'], "password": decrypted_password})

        # Build the UI
        for identifier, password_and_id_list in grouped_passwords.items():
            # Identifier label
            identifier_label = QLabel(f"{identifier}:", self)
            identifier_label.setStyleSheet(
                "font-size: 17px; font-weight: bold; color: #FFFF00;")
            passwords_layout.addWidget(identifier_label)

            # Create a row for each password
            for password_and_id in password_and_id_list:
                password_row = QHBoxLayout()

                password_label = QLabel(
                    f"- {password_and_id['password']}", self)
                password_label.setStyleSheet(
                    "font-size: 14px; color: #FFFFFF;")
                password_row.addWidget(password_label)

                password_row.addStretch(1)

                # Delete button for each password 
                delete_button = QPushButton("Delete", self)
                delete_button.setStyleSheet(
                    "background-color: #FF0000; color: #FFFFFF; font-size: 10px;")
                delete_button.setFixedSize(40, 20)
                # Disable focus on the button
                delete_button.setFocusPolicy(Qt.NoFocus)
                delete_button.clicked.connect(
                    lambda _, entry_id=password_and_id['id']: self.delete_password(entry_id))
                password_row.addWidget(delete_button)

                passwords_layout.addLayout(password_row)

        return passwords_widget

    def delete_password(self, entry_id):
        """Delete the password from the JSON file and update the UI."""
        file_path = "passwords.json"
        if os.path.exists(file_path) and os.stat(file_path).st_size > 0:
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Filter out the entry with the matching id
            data = [entry for entry in data if entry['id'] != entry_id]

            # Save the updated data to the file
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

            # Check if no passwords are left in the entire data
            if not data:
                self.close()  # Close the dialog if no passwords are left
            else:
                # Refresh the UI after deletion
                self.refresh_passwords()

    def refresh_passwords(self):
        """Refresh the password list by rebuilding the UI."""
        self.layout().removeWidget(self.layout().itemAt(1).widget())
        all_passwords_widget = self.build_all_passwords_ui()
        self.setup_scroll_area(self.layout(), all_passwords_widget)
