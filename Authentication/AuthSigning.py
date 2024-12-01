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

#make the class for signing in and signing out and signing up
class AuthSigning(QMainWindow): #what should i add to the class name parameters?
    def __init__(self):
        super().__init__()
    
    def login_user(self):
        pass

    def logout_user(self):

        pass

    def sign_up_user(self):

        pass

    def forgot_password(self):

        pass