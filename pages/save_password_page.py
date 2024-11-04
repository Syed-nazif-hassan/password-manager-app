from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout
import json
import os


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

        # Email/Username label and input
        email_username_label = QLabel("Email/Username:", self)
        email_username_label.setStyleSheet("color: #FFFF00;")
        self.email_username_input = QLineEdit(self)
        self.email_username_input.setStyleSheet(
            "background-color: #333333; color: #FFFFFF;")
        self.form_layout.addRow(email_username_label,
                                self.email_username_input)

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

    def save_to_json(self):
        # Get the user input
        username = self.email_username_input.text()
        password = self.password_input.text()

        # Define the file path
        file_path = "passwords.json"

        # Check if the file exists and is not empty
        if os.path.exists(file_path) and os.stat(file_path).st_size > 0:
            with open(file_path, 'r') as file:
                data = json.load(file)
        else:
            # If the file doesn't exist or is empty, initialize an empty list
            data = []

        # Append the new username and password to the data
        data.append({"username": username, "password": password})

        # Save the updated data back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        # Clear the input fields after saving
        self.email_username_input.clear()
        self.password_input.clear()
