from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QFormLayout,
    QStackedWidget,
)
from PySide6.QtGui import QIcon
import sys


class PasswordManagerApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title and fixed size
        self.setWindowTitle("Password Manager")
        self.setStyleSheet("background-color: #000000;")  # Set background color for the window
        self.setFixedSize(400, 300)
        
        # Set window icon
        self.setWindowIcon(QIcon("icon.png"))

        # Create a stacked widget to manage multiple pages
        self.stacked_widget = QStackedWidget(self)

        # Create the first page
        self.save_password_page = QWidget()
        self.init_save_password_page()

        # Create the second page
        self.get_password_page = QWidget()
        self.init_get_password_page()

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.save_password_page)
        self.stacked_widget.addWidget(self.get_password_page)

        # Set the stacked widget as the main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.stacked_widget)
        self.setLayout(self.main_layout)

    def init_save_password_page(self):
        # Layout for the password saving page
        layout = QVBoxLayout()

        # Main title label
        title_label = QLabel("Password Manager", self)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFF00;")
        layout.addWidget(title_label)

        # Form layout
        self.form_layout = QFormLayout()

        # Email/Username label and input
        email_username_label = QLabel("Email/Username:", self)
        email_username_label.setStyleSheet("color: #FFFF00;")
        self.email_username_input = QLineEdit(self)
        self.email_username_input.setStyleSheet("background-color: #333333; color: #FFFFFF;")
        self.form_layout.addRow(email_username_label, self.email_username_input)

        # Password label and input
        password_label = QLabel("Password:", self)
        password_label.setStyleSheet("color: #FFFF00;") 
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # To mask password input
        self.password_input.setStyleSheet("background-color: #333333; color: #FFFFFF;")
        self.form_layout.addRow(password_label, self.password_input)

        # Submit button
        submit_button = QPushButton("Save", self)
        submit_button.setStyleSheet("background-color: #007BFF; color: #FFFFFF;")
        self.form_layout.addRow("", submit_button)
        
        layout.addLayout(self.form_layout)

        # Button to switch to get password page
        switch_to_get_password_page = QPushButton("Get Password", self)
        switch_to_get_password_page.setStyleSheet("background-color: #4CAF50; color: #FFFFFF;")
        switch_to_get_password_page.clicked.connect(self.get_password)
        layout.addWidget(switch_to_get_password_page)

        self.save_password_page.setLayout(layout)

    def init_get_password_page(self):
        # Layout for the password getting page
        layout = QVBoxLayout()

        # Title label for the password getting page
        title_label = QLabel("Password Manager", self)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFF00;")
        layout.addWidget(title_label)
        
        # Form layout
        self.form_layout = QFormLayout()

        # Email/Username label and input
        email_username_label = QLabel("Email/Username:", self)
        email_username_label.setStyleSheet("color: #FFFF00;") 
        self.email_username_input = QLineEdit(self)
        self.email_username_input.setStyleSheet("background-color: #333333; color: #FFFFFF;")
        self.form_layout.addRow(email_username_label, self.email_username_input)

        # Get button
        get_button = QPushButton("Get", self)
        get_button.setStyleSheet("background-color: #007BFF; color: #FFFFFF;")
        self.form_layout.addRow("", get_button)
        
        layout.addLayout(self.form_layout)

        # Button to switch back to the password saving page
        switch_to_save_password_page = QPushButton("Save Password", self)
        switch_to_save_password_page.setStyleSheet("background-color: #4CAF50; color: #FFFFFF;")
        switch_to_save_password_page.clicked.connect(self.save_password)
        layout.addWidget(switch_to_save_password_page)

        self.get_password_page.setLayout(layout)

    def save_password(self):
        # Show the password saving page
        self.stacked_widget.setCurrentWidget(self.save_password_page)

    def get_password(self):
        # Show the password getting page
        self.stacked_widget.setCurrentWidget(self.get_password_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the main window
    window = PasswordManagerApp()
    window.show()

    # Start the event loop
    sys.exit(app.exec())
