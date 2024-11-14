from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout
from PySide6.QtCore import QTimer, Qt
from pages.show_passwords_dialog import ShowPasswordsDialog
from security import decrypt_identifier
import json
import os


class GetPasswordPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Reference to main window
        # Get stacked_widget from the main window
        self.stacked_widget = main_window.stacked_widget

        # Layout for the password getting page
        layout = QVBoxLayout()

        # Title label for the password getting page
        title_label = QLabel("Password Manager", self)
        title_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #FFFF00;")
        layout.addWidget(title_label)

        # Form layout
        self.form_layout = QFormLayout()

        # identifier label and input
        identifier_label = QLabel("Identifier:", self)
        identifier_label.setStyleSheet("color: #FFFF00;")
        self.identifier_input = QLineEdit(self)
        self.identifier_input.setStyleSheet(
            "background-color: #333333; color: #FFFFFF;")
        self.form_layout.addRow(identifier_label,
                                self.identifier_input)

        # Get button
        get_button = QPushButton("Get", self)
        get_button.setStyleSheet(
            "background-color: #007BFF; color: #FFFFFF; outline: none")
        # Disable focus for this button
        get_button.setFocusPolicy(Qt.NoFocus)
        # Connect to show_user_passwords function
        get_button.clicked.connect(self.show_user_passwords)
        self.form_layout.addRow("", get_button)

        layout.addLayout(self.form_layout)

        # Button to switch back to the password saving page
        switch_to_save_password_page = QPushButton("Save Password", self)
        switch_to_save_password_page.setStyleSheet(
            "background-color: #4CAF50; color: #FFFFFF;")
        switch_to_save_password_page.clicked.connect(
            self.main_window.save_password)
        layout.addWidget(switch_to_save_password_page)

        self.setLayout(layout)

        # Error label to show messages (initially empty)
        self.error_label = QLabel("", self)
        self.error_label.setStyleSheet("color: red;")
        self.form_layout.addRow("", self.error_label)

    def show_user_passwords(self):
        # Identifier to send to 'show_passwords_dialog.py'
        identifier_to_send = None

        # Clear any previous error message
        self.error_label.setText("")

        # Get the input from the form
        entered_identifier = self.identifier_input.text().strip()

        # Check if the input is empty
        if not entered_identifier:
            # Display error message if the input is empty
            self.error_label.setText("Please enter a identifier.")

            # Set a timer to clear the error message after 3 seconds (3000 milliseconds)
            QTimer.singleShot(3000, self.clear_error_message)
            return  # Stop further processing if input is empty

        # Define the file path
        file_path = "passwords.json"

        # Check if the file exists and is not empty
        if os.path.exists(file_path) and os.stat(file_path).st_size > 0:
            with open(file_path, 'r') as file:
                data = json.load(file)
        else:
            data = []

        # Search for the entered identifier in the loaded data
        password_and_ids = []
        for entry in data:
            # Identifier in encrypted form
            encrypted_identifier = entry['identifier']

            # Password in encrypted form
            encrypted_password = entry['password']

            # Decrypt the identifier before comparison
            decrypted_identifier = decrypt_identifier(encrypted_identifier)

            if decrypted_identifier.strip().lower() == entered_identifier.lower():
                # Update identifier_send_to
                identifier_to_send = encrypted_identifier

                # Append the encrypted password to the list
                password_and_ids.append({"id": entry['id'],
                                        "password": encrypted_password})

        if password_and_ids:
            # Clear the input field
            self.identifier_input.clear()

            # Create and open the modal dialog for passwords
            dialog = ShowPasswordsDialog(
                identifier_to_send, password_and_ids, self.main_window)
            dialog.exec_()  # This will block the main window until the dialog is closed
        else:
            # Update the error message if identifier is not found
            self.error_label.setText("Identifier not found!")

            # Set a timer to clear the error message after 3 seconds (3000 milliseconds)
            QTimer.singleShot(3000, self.clear_error_message)

    # Function to clear the error label
    def clear_error_message(self):
        self.error_label.setText("")
