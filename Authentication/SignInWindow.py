import sys
import hashlib
import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from supabase import create_client, Client
from dotenv import load_dotenv
from PySide6.QtNetwork import QSslConfiguration
from PySide6.QtCore import Signal

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

#class for authentication and auth ui
class SignInWindow(QWidget):
    login_successful = Signal()

    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 500, 400)
        # Connect to the main window's close_all_windows_signal
        main_window.close_all_windows_signal.connect(self.close)
        self.setup_ui()

    def setup_ui(self):
        # Create layout
        auth_layout = QVBoxLayout()


        #2 create the widgets needed for the auth window
                # add widgets to the layout
        #1 email
        self.email_signin_label = QLabel("Email")
        self.email_signin = QLineEdit()
        self.email_signin.setPlaceholderText("Email")
        self.email_signin.setObjectName("email_signin")
        auth_layout.addWidget(self.email_signin_label)
        auth_layout.addWidget(self.email_signin)
        #email_signin.textChanged.connect(self.email_signin_changed)
        
        #2 password
        self.user_password_label = QLabel("Password")
        self.user_password = QLineEdit()
        self.user_password.setPlaceholderText("Password")
        self.user_password.setObjectName("user_password")
        #i want the minimum length of the password to be 5 characters

        #the password should be hidden
        self.user_password.setEchoMode(QLineEdit.Password)
        auth_layout.addWidget(self.user_password_label)
        auth_layout.addWidget(self.user_password)

        #3 login button
 
        self.login_button = QPushButton("Login")
        self.login_button.setObjectName("login_button")
        # login_button.mousePressEvent = self.login_button_clicked
        # TODO #I want the login button to be enabled only when the email and password are valid

        #I want the login button to be blue
        self.login_button.setStyleSheet("background-color: #1abc9c; color: white;")
        self.login_button.clicked.connect(self.login_user)
        auth_layout.addWidget(self.login_button)

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
    
    # def login_user(self):
    #     """
    #     Authenticates a user based on the provided email and password.
        
    #     Retrieves the email and password input from the login form, performs
    #     validation, and emits a signal if the login is successful. Displays a 
    #     warning message if the credentials are invalid.

    #     :return: None
    #     """
    #     email = self.email_signin.text()
    #     password = self.user_password.text()

    #     if not email or not password:
    #         QMessageBox.warning(self, "Login Failed", "Please enter both email and password.")
    #         return
        
    #     #retrieve the email and password from supabase
    #     user_response = supabase.table('users', schema='public').select('*').eq('email', email).single().execute()


    #     if user_response.get('error') or not user_response.get('data'):
    #         QMessageBox.warning(self, "Login Error", "Invalid email or password.")
    #         return
        
    #     user = user_response['data']
    #     salt = user['salt']
    #     stored_hash_password = user['hash_password']

    #     #hash the password with sha-3 awith the retrieved salt
    #     hashed_password = hashlib.sha3_256((password + salt).encode()).hexdigest()

    #     if hashed_password == stored_hash_password:
    #         #login the user
    #         response = supabase.auth.sign_in(
    #             {
    #                 "email": email,
    #                 "password": hashed_password
    #             }
    #         )

    #         if response.get('error'):
    #             QMessageBox.warning(self, "Login Error", response['error']['message'])
    #             return

    #         else:
    #             QMessageBox.information(self, "Login Successful", "You have successfully logged in.")
    #             #if the login is successful, emit the login_successful signal
    #             self.login_successful.emit()

    #     else:
    #         QMessageBox.warning(self, "Login Error", "Invalid email or password.")


    def login_user(self):
        email = self.email_signin.text()
        password = self.user_password.text()

        if not email or not password:
            QMessageBox.warning(self, "Login Failed", "Please enter both email and password.")
            return

        try:
            # Use Supabase Auth API for login
            response = supabase.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password
                }
            )

            if response.user:
                QMessageBox.information(self, "Login Successful", f"Welcome {response.user.email}!")
                self.login_successful.emit()
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid credentials. Please try again.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            