from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout


class GetPasswordPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window  # Reference to main window

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
