import sys
import hashlib
import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from supabase import create_client, Client
from dotenv import load_dotenv
from PySide6.QtNetwork import QSslConfiguration
from EmployeeEditorPage.MainMethods import MainMethods  # Import your main window class here
from PySide6.QtCore import Signal


#class for authentication and auth ui
class SignInWindow(QWidget):
    login_successful = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 500, 400)
        self.setup_ui()

    def setup_ui(self):
        # Create layout
        auth_layout = QVBoxLayout()


        #2 create the widgets needed for the auth window
                # add widgets to the layout
        #1 email
        self.email_signin_label = QLabel("Email")
        email_signin = QLineEdit()
        email_signin.setPlaceholderText("Email")
        email_signin.setObjectName("email_signin")
        auth_layout.addWidget(self.email_signin_label)
        auth_layout.addWidget(email_signin)
        #email_signin.textChanged.connect(self.email_signin_changed)
        
        #2 password
        self.user_password_label = QLabel("Password")
        user_password = QLineEdit()
        user_password.setPlaceholderText("Password")
        user_password.setObjectName("user_password")
        #i want the minimum length of the password to be 5 characters

        #the password should be hidden
        user_password.setEchoMode(QLineEdit.Password)
        auth_layout.addWidget(self.user_password_label)
        auth_layout.addWidget(user_password)

        #3 login button
 
        login_button = QPushButton("Login")
        login_button.setObjectName("login_button")
        # login_button.mousePressEvent = self.login_button_clicked
        # TODO #I want the login button to be enabled only when the email and password are valid

        #I want the login button to be blue
        login_button.setStyleSheet("background-color: #1abc9c; color: white;")
        login_button.clicked.connect(self.login_user)
        auth_layout.addWidget(login_button)

        #4 register button        
        self.sign_up_button = QPushButton("Sign Up")
        self.sign_up_button.setObjectName("register_button")
        self.sign_up_button.clicked.connect(self.open_sign_up)
        self.sign_up_button.setStyleSheet("background-color: #4c7f99; color: white;")

        auth_layout.addWidget(self.sign_up_button)

        self.forgot_password_button = QPushButton("Forgot Password")
        self.forgot_password_button.setStyleSheet("background-color: #5c7f99; color: white;")
        self.forgot_password_button.clicked.connect(self.open_forgot_password)
        auth_layout.addWidget(self.forgot_password_button)

        # declare the layout
        self.setLayout(auth_layout)


    def open_sign_up(self):
        from Authentication.SignUp import SignUp
        self.sign_up_window = SignUp()
        self.sign_up_window.show()

    def open_forgot_password(self):
        from Authentication.ForgotPassword import ForgotPassword
        self.forgot_password_window = ForgotPassword()
        self.forgot_password_window.show()

    '''
    
    def login_user(self):
        # Placeholder login logic - Replace with real authentication
        email = self.email_signin.text()
        password = self.user_password.text()

        if email == "test@example.com" and password == "password":  # Dummy validation
            self.login_successful.emit()  # Emit signal for successful login
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials. Please try again.")
    '''
    
    def login_user(self):
        """
        Authenticates a user based on the provided email and password.
        
        Retrieves the email and password input from the login form, performs
        validation, and emits a signal if the login is successful. Displays a 
        warning message if the credentials are invalid.

        :return: None
        """
        pass



        