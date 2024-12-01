import sys
import hashlib
import os
import secrets
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from supabase import create_client, Client
from dotenv import load_dotenv
from PySide6.QtNetwork import QSslConfiguration

#initialize supabase client
# Load environment variables
load_dotenv()

# Access environment variables
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Set up SSL configuration later
# ssl_config = QSslConfiguration()
# ssl_config.setPeerVerifyMode(QSslSocket.PeerVerifyDisabled)

###TODO
#make this Authentication folder close completely and only show the main window
#make this Authentication folder close and logout when the main window is closed


#make the class for signing up
class SignUp(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.setWindowTitle("Sign Up")
        self.resize(400, 300)

        # Connect to the main window's close_all_windows_signal
        main_window.close_all_windows_signal.connect(self.close)

        self.setup_ui()

        # Create widgets

    def setup_ui(self):
        layout = QVBoxLayout()

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.sign_up_button = QPushButton("Sign Up")
        self.sign_up_button.clicked.connect(self.signup_user)
        layout.addWidget(self.sign_up_button)

        self.setLayout(layout)

    def signup_user(self):
        """
        Handles user registration by creating a new user account in the database.
        Retrieves the registration form data, performs validation, and emits a signal if
        the registration is successful. Displays a warning message if the credentials are
        invalid.

        :return: None
        """
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Signup Failed", "Please enter both email and password.")
            return

        # Generate a random salt
        salt = secrets.token_hex(16)
        # Hash the password with SHA-3 and add the salt
        hash_password = hashlib.sha3_256((password + salt).encode()).hexdigest()

        try:
            # Store the user in Supabase
            response = supabase.auth.sign_up({"email": email, "password": password})

            # Check if user is created
            if response.user:
                QMessageBox.information(self, "Signup Successful", "Account created successfully.")
                self.close()
            else:
                QMessageBox.warning(self, "Signup Failed", "Could not create an account. Please try again.")

        except Exception as e:
            # Handle unexpected errors
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
