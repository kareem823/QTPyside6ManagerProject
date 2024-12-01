import sys
import hashlib
import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from supabase import create_client, Client
from dotenv import load_dotenv
from PySide6.QtNetwork import QSslConfiguration


#class for authentication and auth ui
class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authentication")
        self.setGeometry(100, 100, 500, 400)
        self.setup_ui()

    def setup_ui(self):
        # Create layout
        auth_layout = QVBoxLayout()

        #2 create the widgets needed for the auth window
                # add widgets to the layout
        #1 email
        self.email_signin_label = QLabel("Email")
        auth_layout.addWidget(self.email_signin_label)
        email_signin = QLineEdit()
        email_signin.setPlaceholderText("Email")
        email_signin.setObjectName("email_signin")
        auth_layout.addWidget(email_signin)
        #email_signin.textChanged.connect(self.email_signin_changed)
        
        #2 password
        self.user_password_label = QLabel("Password")
        auth_layout.addWidget(self.user_password_label)
        user_password = QLineEdit()
        user_password.setPlaceholderText("Password")
        user_password.setObjectName("user_password")
        #i want the minimum length of the password to be 5 characters
        user_password.setMinimumLength(5)
        #the password should be hidden
        user_password.setEchoMode(QLineEdit.Password)
        auth_layout.addWidget(user_password)

        #3 login button
 
        login_button = QPushButton("Login")
        login_button.setObjectName("login_button")
        # login_button.mousePressEvent = self.login_button_clicked
        #I want the login button to be enabled only when the email and password are valid
        login_button.setEnabled(False)
        #I want the login button to be blue
        login_button.setStyleSheet("background-color: #1abc9c; color: white;")
        login_button.clicked.connect(self.login_user)
        auth_layout.addWidget(login_button)

        #4 register button
        register_button = QPushButton("Register")
        register_button.setObjectName("register_button")
        register_button.setStyleSheet("background-color: #4c7f99; color: white;")
        register_button.clicked.connect(self.register_user)
        auth_layout.addWidget(register_button)

        #5 forgot password
        #I want a link to the forgot password page
        forgot_password_button = QPushButton("Forgot Password")
        forgot_password_button.setObjectName("forgot_password_button")
        forgot_password_button.setStyleSheet("background-color: #2c3e50; color: white;")
        forgot_password_button.clicked.connect(self.forgot_password)
        auth_layout.addWidget(forgot_password_button)

        # declare the layout
        self.setLayout(auth_layout)



