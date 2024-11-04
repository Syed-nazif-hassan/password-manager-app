from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class ShowPasswordsPage(QWidget):
    def __init__(self, main_window, username, passwords):
        super().__init__()
        self.main_window = main_window  # Reference to main window

        # Layout for displaying passwords
        layout = QVBoxLayout()

        # Title label for the username
        title_label = QLabel(f"Passwords for {username}:", self)
        title_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #FFFF00;")
        layout.addWidget(title_label)

        # Display each password
        for password in passwords:
            password_label = QLabel(password, self)
            password_label.setStyleSheet("color: #FFFFFF;")
            layout.addWidget(password_label)

        # Set the layout
        self.setLayout(layout)
