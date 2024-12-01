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
from Authentication.SignInWindow import SignInWindow

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

class ForgotPassword(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Forgot Password")
        self.setGeometry(100, 100, 500, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        #make the email input field
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        #make the reset password button
        self.reset_password_button = QPushButton("Reset Password")
        self.reset_password_button.clicked.connect(self.reset_password)
        layout.addWidget(self.reset_password_button)

        #make the back to sign in button
        self.back_to_sign_in_button = QPushButton("Back to Sign In")
        self.back_to_sign_in_button.clicked.connect(self.back_to_sign_in)
        layout.addWidget(self.back_to_sign_in_button)

        self.setLayout(layout)

    def reset_password(self):
        pass

    def back_to_sign_in(self):
        self.sign_in_window = SignInWindow()
        self.sign_in_window.show()