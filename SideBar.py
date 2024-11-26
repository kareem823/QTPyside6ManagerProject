from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from DBModel import Employee, Session, session
from MainMethods import *

# Sidebar Class
class Sidebar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self.setStyleSheet("background-color: #2c3e50; color: white;")
        self.sidebar_layout = QVBoxLayout(self)

        # give the side bar a title
        title_label = QLabel(f"{parent.company_name}")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; padding-bottom: 5px; padding-top: 5px; padding-left: 5px; padding-right: 5px")
        self.sidebar_layout.addWidget(title_label)

        # Navigation Menu
        self.manage_employees_button = QComboBox()
        self.manage_employees_button.addItems(["Manage Employees"])
        self.manage_employees_button.setStyleSheet("QComboBox { color: white; padding: 30px; text-align: left; } QComboBox:hover { background-color: #34495e; }")
        self.sidebar_layout.addWidget(self.manage_employees_button)

        self.manage_finances_button = QComboBox()
        self.manage_finances_button.addItems(["Manage Finances"])
        self.manage_finances_button.setStyleSheet("QComboBox { color: white; padding: 30px; text-align: left; } QComboBox:hover { background-color: #34495e; }")
        self.sidebar_layout.addWidget(self.manage_finances_button)

        # Add a settings button
        self.settings_button = QPushButton("Settings")
        self.settings_button.setStyleSheet("QPushButton { color: white; padding: 30px; text-align: left; } QPushButton:hover { background-color: #34495e; }")
        self.sidebar_layout.addWidget(self.settings_button)

        # Add a logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.setStyleSheet("QPushButton { color: white; padding: 30px; text-align: left; } QPushButton:hover { background-color: #34495e; }")
        self.sidebar_layout.addWidget(self.logout_button)

        # Add toggle button to the sidebar in hamburger menu style 
        self.toggle_sidebar_button = QPushButton("Hide Sidebar")
        self.toggle_sidebar_button.setStyleSheet("background-color: #1abc9c; color: white;")
        self.toggle_sidebar_button.clicked.connect(parent.toggle_sidebar)
        self.sidebar_layout.addWidget(self.toggle_sidebar_button)
