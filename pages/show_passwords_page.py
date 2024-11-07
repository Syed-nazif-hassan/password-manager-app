from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea


class ShowPasswordsPage(QWidget):
    def __init__(self, main_window, identifier, passwords):
        super().__init__()
        self.main_window = main_window  # Reference to main window

        # Layout for displaying passwords
        layout = QVBoxLayout()

        # Title label for the identifier
        title_label = QLabel(f"Password{'s' if len(
            passwords) > 1 else ''} for {identifier}:", self)
        title_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #FFFF00;")
        layout.addWidget(title_label)

        # Create a QWidget to hold the passwords (to use with QScrollArea)
        password_widget = QWidget(self)
        password_layout = QVBoxLayout(password_widget)

        # Display each password
        for password in passwords:
            password_label = QLabel(f"- {password}", self)
            password_label.setStyleSheet("color: #FFFFFF;")
            password_layout.addWidget(password_label)

        # Create a QScrollArea
        scroll_area = QScrollArea(self)
        scroll_area.setWidget(password_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Set the layout
        self.setLayout(layout)
