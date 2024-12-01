from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from DBModel import Employee, Session, session
from EmployeeEditorPage.MainMethods import *
# from Authentication.SignInWindow import SignInWindow
from supabase import create_client, Client
from dotenv import load_dotenv
from PySide6.QtNetwork import QSslConfiguration
from PySide6.QtCore import Signal
import os

#initialize supabase client
# Load environment variables
load_dotenv(dotenv_path="authentication/.env")

# Access environment variables
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Sidebar Class
class Sidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self.setStyleSheet("background-color: #2c3e50; color: white;")
        self.sidebar_layout = QVBoxLayout(self)


        # give the side bar a title
        title_label = QLabel(f"{parent.company_name}")
        title_label.setStyleSheet("""font-size: 32px; 
                                  font-weight: bold; 
                                  padding-bottom: 5px; 
                                  padding-top: 5px; padding-left: 5px; 
                                  padding-right: 5px""")
        self.sidebar_layout.addWidget(title_label)

        # Navigation Menu
        self.manage_employees_button = QPushButton()
        self.manage_employees_button.setText("Manage Employees")
        self.manage_employees_button.setStyleSheet("""QPushButton { font-size: 16px;
                                                   color: white; padding: 20px; text-align: left; 
                                                   } 
                                                   QPushButton:hover { background-color: #34495e; }""")
        self.sidebar_layout.addWidget(self.manage_employees_button)
        self.manage_employees_button.clicked.connect(parent.show_manage_employees)


        self.manage_finances_button = QPushButton()
        self.manage_finances_button.setText("Manage Finances")
        self.manage_finances_button.setStyleSheet("""QPushButton { font-size: 16px;
                                                  color: white; padding: 20px; text-align: left;
                                                   } QPushButton:hover 
                                                  { background-color: #34495e; }""")
        self.sidebar_layout.addWidget(self.manage_finances_button)
        self.manage_finances_button.clicked.connect(parent.show_manage_finances)

        # # Add a button to the side bar for notes page
        # self.notes_button = QPushButton()
        # self.notes_button.setText("Notes")
        # self.notes_button.setStyleSheet("""QPushButton { font-size: 16px;
        #                                 color: white; padding: 20px; text-align: left;
        #                                  } QPushButton:hover
        #                                 { background-color: #34495e; }""")
        # self.sidebar_layout.addWidget(self.notes_button)

        '''
        OTHER THINGS TO ADD IN THE FUTURE:
        Time Tracking Tools (e.g., Toggl, Harvest):

        These applications allow users to track how much time is spent on various tasks and
        projects, helping to identify areas for improvement and optimize productivity.

        Virtual Assistant Services (e.g., Time Etc, Belay):

        Hiring a virtual assistant can help manage administrative tasks, schedule meetings, 
        and handle other time-consuming activities, freeing up the CEO's
         time for strategic decision-making.

        Mind Mapping Software (e.g., MindMeister, XMind):

        These tools help visualize ideas and strategies, making it easier to brainstorm and
        organize thoughts for presentations or planning sessions.

        '''

        # Add a settings button
        self.settings_button = QPushButton("Settings")
        self.settings_button.setStyleSheet("""QPushButton { font-size: 16px;
                                                  color: white; padding: 20px; text-align: left;
                                                   } QPushButton:hover 
                                                  { background-color: #34495e; }""")
        self.sidebar_layout.addWidget(self.settings_button)
        #self.settings_button.clicked.connect(parent.show_settings)

        # Add a logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.setStyleSheet("""QPushButton { font-size: 16px;
                                          color: white; padding: 20px; text-align: left; } 
                                         QPushButton:hover { background-color: #34495e; }""")
        # self.logout_button.clicked.connect(self.signout)
        self.sidebar_layout.addWidget(self.logout_button)

        # Add toggle button to the sidebar in hamburger menu style 
        self.toggle_sidebar_button = QPushButton("Hide Sidebar")
        self.toggle_sidebar_button.setStyleSheet("background-color: #1abc9c; color: white;")
        self.toggle_sidebar_button.clicked.connect(parent.toggle_sidebar)
        self.sidebar_layout.addWidget(self.toggle_sidebar_button)


        
    # def signout(self):
    #     """Log out the user and close all windows."""
    #     try:
    #         # Perform Supabase logout
    #         supabase.auth.sign_out()
    #         QMessageBox.information(self, "Sign Out", "You have successfully signed out.")

    #         # Close the main window to trigger full application closure
    #         parent = self.parent()
    #         if parent:
    #             parent.close()

    #     # Close the main window to trigger the closure of all child windows
    #         self.parent().close()

    #     except Exception as e:
    #         QMessageBox.critical(self, "Sign Out Failed", f"An error occurred: {e}")
