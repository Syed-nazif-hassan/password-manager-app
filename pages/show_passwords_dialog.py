from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QWidget,
    QLabel,
    QVBoxLayout,
    QScrollArea,
    QHBoxLayout,
    QPushButton
)
from PySide6.QtCore import Qt
import json
import os


class ShowPasswordsDialog(QDialog):
    def __init__(self, identifier, passwords, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Password Manager")
        self.setModal(True)  # Set as a modal dialog
        self.identifier = identifier  # Store the identifier
        self.passwords = passwords  # Store passwords so we can update them

        # Layout for displaying passwords
        layout = QVBoxLayout()

        # Create a QWidget to hold the passwords
        password_widget = self.build_password_list_ui()

        # Set up the title label
        self.setup_title_label(layout)

        # Set up the scroll area
        self.setup_scroll_area(layout, password_widget)

        # Set up the "All Passwords" button
        self.setup_all_passwords_button(layout)

        # Set the layout
        self.setLayout(layout)

        # Set the dialog size to match the main window
        if parent is not None:
            self.resize(parent.size())

    def setup_title_label(self, layout):
        """Set up the title label"""
        title_label = QLabel(f"Password{'s' if len(self.passwords) > 1 else ''} for {
                             self.identifier}:", self)
        title_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #FFFF00;")
        layout.addWidget(title_label)

    def setup_all_passwords_button(self, layout):
        """Set up the 'All Passwords' button"""
        all_passwords_button = QPushButton("Show All Passwords", self)
        all_passwords_button.setStyleSheet(
            "background-color: #007BFF; color: #FFFFFF;")
        layout.addWidget(all_passwords_button)

    def setup_scroll_area(self, layout, password_widget):
        """Set up the scroll area"""
        scroll_area = QScrollArea(self)
        scroll_area.setWidget(password_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

    def build_password_list_ui(self):
        """Builds the list of password rows."""
        password_widget = QWidget(self)
        password_layout = QVBoxLayout(password_widget)

        # Display each password with copy and delete buttons
        for password in self.passwords:
            password_row = QHBoxLayout()

            password_label = QLabel(f"- {password}", self)
            password_label.setStyleSheet("font-size: 14px; color: #FFFFFF;")
            password_row.addWidget(password_label)

            password_row.addStretch(1)

            # Copy button
            copy_button = QPushButton("Copy", self)
            copy_button.setStyleSheet(
                "background-color: #008000; color: #FFFFFF; font-size: 10px;")
            copy_button.setFocusPolicy(Qt.NoFocus)
            copy_button.setFixedSize(40, 20)
            copy_button.clicked.connect(
                lambda _, p=password: self.copy_password(p))
            password_row.addWidget(copy_button)

            # Delete button
            delete_button = QPushButton("Delete", self)
            delete_button.setStyleSheet(
                "background-color: #FF0000; color: #FFFFFF; font-size: 10px;")
            delete_button.setFocusPolicy(Qt.NoFocus)
            delete_button.setFixedSize(40, 20)
            delete_button.clicked.connect(
                lambda _, p=password: self.delete_password(p))
            password_row.addWidget(delete_button)

            password_layout.addLayout(password_row)

        return password_widget

    def delete_password(self, password):
        """Delete the selected password from the list and JSON file, and update the UI."""
        # Remove the password from the list
        self.passwords.remove(password)

        # Remove the password from the JSON file
        self.remove_password_from_json(password)

        # If all passwords are deleted, close the dialog
        if not self.passwords:
            self.close()  # Close the dialog
        else:
            # Update the displayed list of passwords
            self.update_password_list()

    def remove_password_from_json(self, password):
        """Remove the password from the JSON file."""
        file_path = "passwords.json"

        if os.path.exists(file_path) and os.stat(file_path).st_size > 0:
            with open(file_path, 'r') as file:
                data = json.load(file)

            for entry in data:
                if entry['identifier'] == self.identifier:
                    if password in entry['passwords']:
                        entry['passwords'].remove(password)
                    if not entry['passwords']:
                        # Remove entry if no passwords are left
                        data.remove(entry)
                    break

            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

    def copy_password(self, password):
        """Copy the selected password to the clipboard."""
        clipboard = QApplication.clipboard()
        clipboard.setText(password)

    def update_password_list(self):
        """Update the list of passwords displayed in the dialog."""
        # Clear the current layout and rebuild it with the updated passwords
        layout = self.layout()

        # Remove all widgets from the layout
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Rebuild the password list UI
        password_widget = self.build_password_list_ui()

        # Set up the title label
        self.setup_title_label(layout)

        # Set up the scroll area
        self.setup_scroll_area(layout, password_widget)

        # Set up the "All Passwords" button
        self.setup_all_passwords_button(layout)
