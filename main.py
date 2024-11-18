from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget
from PySide6.QtGui import QIcon
from pages.save_password_page import SavePasswordPage
from pages.get_passwords_page import GetPasswordPage
import sys


class PasswordManagerApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title and fixed size
        self.setWindowTitle("Password Manager")
        self.setStyleSheet("background-color: #000000;")
        self.setFixedSize(400, 300)

        # Set window icon
        self.setWindowIcon(QIcon("icon/window_icon.png"))

        # Create a stacked widget to manage multiple pages
        self.stacked_widget = QStackedWidget(self)

        # Create the first page (from external file)
        self.save_password_page = SavePasswordPage(self)

        # Create the second page (from external file)
        self.get_password_page = GetPasswordPage(self)

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.save_password_page)
        self.stacked_widget.addWidget(self.get_password_page)

        # Set the stacked widget as the main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.stacked_widget)
        self.setLayout(self.main_layout)

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
