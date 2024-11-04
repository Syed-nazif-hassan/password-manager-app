from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout
from pages.show_passwords_page import ShowPasswordsPage
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

        # Email/Username label and input
        email_username_label = QLabel("Email/Username:", self)
        email_username_label.setStyleSheet("color: #FFFF00;")
        self.email_username_input = QLineEdit(self)
        self.email_username_input.setStyleSheet(
            "background-color: #333333; color: #FFFFFF;")
        self.form_layout.addRow(email_username_label,
                                self.email_username_input)

        # Get button
        get_button = QPushButton("Get", self)
        get_button.setStyleSheet("background-color: #007BFF; color: #FFFFFF;")
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

    def show_user_passwords(self):
        # Get the input username from the form
        entered_username = self.email_username_input.text().strip()

        # Define the file path
        file_path = "passwords.json"

        # Check if the file exists and is not empty
        if os.path.exists(file_path) and os.stat(file_path).st_size > 0:
            with open(file_path, 'r') as file:
                data = json.load(file)
        else:
            data = []

        # Search for the entered username in the loaded data
        found_passwords = [entry['password'] for entry in data if entry['username'].strip(
        ).lower() == entered_username.lower()]

        if found_passwords:
            # Create a new page to show the passwords
            show_passwords_page = ShowPasswordsPage(
                self, entered_username, found_passwords)
            self.stacked_widget.addWidget(show_passwords_page)
            self.stacked_widget.setCurrentWidget(show_passwords_page)
        else:
            # Show message if username is not found
            error_label = QLabel("Username not found!", self)
            error_label.setStyleSheet("color: red;")
            self.form_layout.addRow("", error_label)
