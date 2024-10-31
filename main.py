from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout
import sys

class PasswordManagerApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("Password Manager")
        
        # Set fixed size for the window (width, height)
        self.setFixedSize(400, 300)  # Example: 400x300 pixels

        # Main title label
        self.title_label = QLabel("Password Manager", self)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center;")

        # Form layout for inputs
        self.form_layout = QFormLayout()

        # Email label and input
        self.email_label = QLabel("Email/Username:", self)
        self.email_input = QLineEdit(self)
        self.form_layout.addRow(self.email_label, self.email_input)

        # Password label and input
        self.password_label = QLabel("Password:", self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # To mask password input
        self.form_layout.addRow(self.password_label, self.password_input)

        # Submit button
        self.submit_button = QPushButton("Save", self)

        # Layout to hold everything
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.submit_button)

        # Set layout for the window
        self.setLayout(self.main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create the main window
    window = PasswordManagerApp()
    window.show()

    sys.exit(app.exec())
