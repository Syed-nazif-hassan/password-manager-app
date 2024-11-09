from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout
import json
import os
from PySide6.QtCore import QTimer, Qt


class SavePasswordPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Reference to main window

        # Layout for the password saving page
        layout = QVBoxLayout()

        # Main title label
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

        # Password label and input
        password_label = QLabel("Password:", self)
        password_label.setStyleSheet("color: #FFFF00;")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(
            QLineEdit.Password)  # To mask password input
        self.password_input.setStyleSheet(
            "background-color: #333333; color: #FFFFFF;")
        self.form_layout.addRow(password_label, self.password_input)

        # Submit button
        submit_button = QPushButton("Save", self)
        submit_button.setStyleSheet(
            "background-color: #007BFF; color: #FFFFFF;")
        # Disable focus for this button
        submit_button.setFocusPolicy(Qt.NoFocus)
        # Connect button to save function
        submit_button.clicked.connect(self.save_to_json)
        self.form_layout.addRow("", submit_button)

        layout.addLayout(self.form_layout)

        # Button to switch to get password page
        switch_to_get_password_page = QPushButton("Get Password", self)
        switch_to_get_password_page.setStyleSheet(
            "background-color: #4CAF50; color: #FFFFFF;")
        switch_to_get_password_page.clicked.connect(
            self.main_window.get_password)
        layout.addWidget(switch_to_get_password_page)

        self.setLayout(layout)

        # Error label to show messages (initially empty)
        self.error_label = QLabel("", self)
        self.error_label.setStyleSheet("color: red;")
        self.form_layout.addRow("", self.error_label)

    def save_to_json(self):
        # Clear any previous error message
        self.error_label.setText("")

        # Get the user input
        identifier = self.identifier_input.text()
        password = self.password_input.text()

        # Check if the identifier or password is empty
        if not identifier and not password:
            self.error_label.setText(
                "Please enter both identifier and password.")

            # Set a timer to clear the error message after 3 seconds (3000 milliseconds)
            QTimer.singleShot(3000, self.clear_error_message)

            # Stop further processing if input is empty
            return
        elif not identifier:
            self.error_label.setText("Please enter a identifier.")

            # Set a timer to clear the error message after 3 seconds (3000 milliseconds)
            QTimer.singleShot(3000, self.clear_error_message)

            # Stop further processing if input is empty
            return
        elif not password:
            self.error_label.setText("Please enter a password.")

            # Set a timer to clear the error message after 3 seconds (3000 milliseconds)
            QTimer.singleShot(3000, self.clear_error_message)

            # Stop further processing if input is empty
            return

        # Define the file path
        file_path = "passwords.json"

        # Check if the file exists and is not empty
        if os.path.exists(file_path) and os.stat(file_path).st_size > 0:
            with open(file_path, 'r') as file:
                data = json.load(file)
        else:
            # If the file doesn't exist or is empty, initialize an empty list
            data = []

        # Search for the identifier in the data
        identifier_exists = False
        for entry in data:
            if entry['identifier'] == identifier:
                # If identifier already exists, add the password to the list of passwords
                entry['passwords'].append(password)
                identifier_exists = True
                break

        # If the identifier does not exist, create a new entry
        if not identifier_exists:
            data.append({"identifier": identifier, "passwords": [password]})

        # Save the updated data back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        # Clear the input fields after saving
        self.identifier_input.clear()
        self.password_input.clear()

    # Function to clear the error label
    def clear_error_message(self):
        self.error_label.setText("")
