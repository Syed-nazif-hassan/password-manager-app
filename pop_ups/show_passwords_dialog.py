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
from pop_ups.all_passwords_dialog import AllPasswordsDialog
from security.security import decrypt_string
import json
import os


class ShowPasswordsDialog(QDialog):
    def __init__(self, identifier, passwords_and_ids, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Password Manager")
        self.setModal(True)  # Set as a modal dialog
        self.identifier = identifier  # Store the identifier
        self.passwords_and_ids = passwords_and_ids  # Store passwords and ids

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

        # Decrypt the identifier for title label
        title_label = QLabel(f"Password{'s' if len(self.passwords_and_ids) > 1 else ''} for {
                             decrypt_string(self.identifier)}:", self)
        title_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #FFFF00;")
        layout.addWidget(title_label)

    def setup_all_passwords_button(self, layout):
        """Set up the 'All Passwords' button"""
        all_passwords_button = QPushButton("Show All Passwords", self)
        all_passwords_button.setStyleSheet(
            "background-color: #007BFF; color: #FFFFFF;")
        all_passwords_button.clicked.connect(
            self.show_all_passwords_dialog)  # Connect to AllPasswordsDialog
        layout.addWidget(all_passwords_button)

    def show_all_passwords_dialog(self):
        """Show the AllPasswordsDialog and close the current dialog."""
        self.close()  # Close the current dialog
        all_passwords_dialog = AllPasswordsDialog(
            self)  # Open AllPasswordsDialog
        all_passwords_dialog.exec()  # Show it as a modal dialog

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
        for password_and_id in self.passwords_and_ids:
            password_row = QHBoxLayout()

            # Decrypt the password
            password_label = QLabel(
                f"- {decrypt_string(password_and_id['password'])}", self)

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
                lambda _, p=decrypt_string(password_and_id['password']): self.copy_password(p))
            password_row.addWidget(copy_button)

            # Delete button
            delete_button = QPushButton("Delete", self)
            delete_button.setStyleSheet(
                "background-color: #FF0000; color: #FFFFFF; font-size: 10px;")
            delete_button.setFocusPolicy(Qt.NoFocus)
            delete_button.setFixedSize(40, 20)
            delete_button.clicked.connect(
                lambda _, id=password_and_id['id']: self.delete_password(id))
            password_row.addWidget(delete_button)

            password_layout.addLayout(password_row)

        return password_widget

    def delete_password(self, id):
        """Delete the selected password from the list and JSON file, and update the UI."""
        # Remove the password from the list
        self.passwords_and_ids = [
            d for d in self.passwords_and_ids if d["id"] != id]

        # Remove the password from the JSON file
        self.remove_password_from_json(id)

        # If all passwords are deleted, close the dialog
        if not self.passwords_and_ids:
            self.close()  # Close the dialog
        else:
            # Update the displayed list of passwords
            self.refresh_dialog_layout()

    def remove_password_from_json(self, id):
        """Remove the password from the JSON file."""
        file_path = "storage/passwords.json"

        if os.path.exists(file_path) and os.stat(file_path).st_size > 0:
            with open(file_path, 'r') as file:
                data = json.load(file)

        for entry in data:
            # Encrypted JSON key (ID)
            encrypted_id_key = list(entry.keys())[0]

            if entry[encrypted_id_key] == id:
                data.remove(entry)

        # Write the updated data back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def copy_password(self, password):
        """Copy the selected password to the clipboard."""
        clipboard = QApplication.clipboard()
        clipboard.setText(password)

    def refresh_dialog_layout(self):
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
