from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from sqlalchemy import distinct
from EmployeeEditorPage.EmployeeManager import *
from DBModel import *
from DBModel import Employee, Session, session
from EmployeeEditorPage.EmployeeDialog import EmployeeDialog
from SideBar import Sidebar
from EmployeeEditorPage.EmployeeTableWidget import EmployeeTableWidget
from EmployeeEditorPage.FileExports import FileExports
import os
from FinanceManager.FinanceManager import FinanceManager
from CompanyListDB import *
from supabase import create_client, Client
from dotenv import load_dotenv
from PySide6.QtNetwork import QSslConfiguration
from Authentication.SignInWindow import SignInWindow
from Authentication.SignUp import SignUp
from Authentication.ForgotPassword import ForgotPassword
from FinanceManager.InvoicesPage import InvoicePage

# #initialize supabase client
# # Load environment variables
# load_dotenv()

# # Access environment variables
# SUPABASE_URL = os.getenv('SUPABASE_URL')
# SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# from FinanceManager.InvoicesPage import InvoicePage
# Main Window Class
class MainMethods(QMainWindow):
        # Signal to notify all child windows to close
    close_all_windows_signal = Signal()

    def __init__(self):
        super().__init__()

        self.child_windows = []  # Keep track of child windows

        # make the global variable for the company name
        self.company_name = "Company"
        # make the global variable for the username
        self.username = "User"

        self.setWindowTitle("Employee Management System")
        self.setGeometry(100, 100, 1300, 600)

        # Connect to the main window's close_all_windows_signal
        # Inside MainWindow class or relevant method
        # child_window = SignInWindow(main_window=self)
        # self.register_child_window(child_window)
        # child_window.show()

        # signup_window = SignUp(main_window=self)
        # self.register_child_window(signup_window)
        # signup_window.show()

        # forgot_password_window = ForgotPassword(main_window=self)
        # self.register_child_window(forgot_password_window)
        # forgot_password_window.show()

        self.setup_ui()

    def setup_ui(self):
        # Main window structure

        ###########################
        self.central_widget = QWidget()
        # Set the central widget as the main widget of the window
        self.setCentralWidget(self.central_widget)

        # Create a horizontal layout for the central widget
        self.main_layout = QHBoxLayout(self.central_widget)

        # Left Sidebar (Collapsible)
        self.sidebar = Sidebar(self)
        self.main_layout.addWidget(self.sidebar)

        #create a QStackedwidget to hold different pages
        self.stacked_widget = QStackedWidget()
        '''The stretch parameter is used to specify how much space the widget should take 
        relative to other widgets in the layout. In this case, a stretch factor of 1 means
         that this widget will take up one unit of space relative to other widgets.'''
        self.main_layout.addWidget(self.stacked_widget, stretch=1)

        #create the employee page
        self.employee_page = QWidget()
        self.setup_employee_page()
        self.stacked_widget.addWidget(self.employee_page)

        #create the finance management page
        self.finance_page = QWidget()
        self.setup_finance_page()
        self.stacked_widget.addWidget(self.finance_page)

        #set the default page to the manage employees page
        self.stacked_widget.setCurrentWidget(self.employee_page)


    def setup_employee_page(self):
        # Main Content Area
        main_content_layout = QVBoxLayout(self.employee_page)

        # Header Section
        header_layout = QHBoxLayout()

        # Add a hamburger button to the header
        # make this button always stay on the left side of the header
        self.hamburger_button = QPushButton()
        self.hamburger_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))
        self.hamburger_button.setFixedWidth(30)
        self.hamburger_button.setFixedHeight(30)
        self.hamburger_button.setStyleSheet("background-color: #1abc9c; color: white;")
        self.hamburger_button.clicked.connect(self.toggle_sidebar)
        self.hamburger_button.setVisible(True)  # Initially hidden
        # Add the hamburger button to the header layout
        header_layout.addWidget(self.hamburger_button)

        # Add a welcome label to the header
        welcome_label = QLabel("Welcome to Employee Management System")
        welcome_label.setStyleSheet("font-size: 16px;")
        # Add the welcome label to the header layout
        header_layout.addWidget(welcome_label)

        self.search_bar = QLabel("Manage your employees with care!")
        #self.search_bar.setFixedWidth(400)
        #self.search_bar.setPlaceholderText("Manage your employees with care!")
        # self.search_bar.textChanged.connect(self.search_employees)
        header_layout.addWidget(self.search_bar)

        # Add the header layout to the main content layout
        main_content_layout.addLayout(header_layout)

        # Employee Info Section
        employee_info_label = QLabel("Employee Info")
        employee_info_label.setStyleSheet("""font-family: Georgia, sans-serif; 
                                          font-size: 20px; font-weight: bold; padding: 10px 0;""")
        main_content_layout.addWidget(employee_info_label)


        # icons for the action buttons
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        # excel_icon_path = os.path.join(current_dir, 'excel_icon.png')
        # pdf_icon_path = os.path.join(current_dir, 'pdf_icon.png')

        # Action Buttons Layout
        action_buttons_layout = QHBoxLayout()

        # Add Employee Button
        self.add_employee_button = QPushButton("Add Employee")
        self.add_employee_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 10px 15px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.add_employee_button.clicked.connect(self.add_employee)
        action_buttons_layout.addWidget(self.add_employee_button)

        # Initialize the file exports class
        self.file_exports = FileExports(self)

        # Export Excel Button
        export_excel_button = QPushButton("Excel Export")
        # excel_icon = QIcon(excel_icon_path)
        # export_excel_button.setIcon(excel_icon)
        export_excel_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 10px 15px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        export_excel_button.clicked.connect(self.file_exports.export_excel)
        action_buttons_layout.addWidget(export_excel_button)

        # Export PDF Button
        export_pdf_button = QPushButton("PDF Export")
        # pdf_icon = QIcon(pdf_icon_path)
        # export_pdf_button.setIcon(pdf_icon)
        export_pdf_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                padding: 10px 15px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        export_pdf_button.clicked.connect(self.file_exports.export_pdf)
        action_buttons_layout.addWidget(export_pdf_button)

        # # Add the action buttons layout to the main content layout
        main_content_layout.addLayout(action_buttons_layout)


        # Filter Controls
        #Need to implement filetering from drop down sections 
        # next and make them show what's in the database for options.
        filter_layout = QHBoxLayout()

        #maybe replace this with another filter or a button later
        # self.gender_dropdown = QComboBox()
        # # make them show what's in the database for options.
        # self.gender_dropdown.addItems(["Select Gender", "Male", "Female"])
        # self.gender_dropdown.currentIndexChanged.connect(self.search_employees)

        # filter_layout.addWidget(self.gender_dropdown)


        self.position_dropdown = QComboBox()

        selected_position = self.position_dropdown.currentText()

        # Add positions to the dropdown from the Employee database
        self.session = Session()
        # # Query distinct positions from the database
        # employees = self.session.query(Employee).filter(Employee.position == selected_position).all()

        #     # Update the employee table with the filtered employees
        # self.table_widget.load_employees(employees)

        distinct_positions = self.session.query(distinct(Employee.position)).all()

        # Extract positions from query result
        positions = [position[0] for position in distinct_positions]

        # Add positions to the dropdown
        self.position_dropdown.addItems(["All Position"] + positions)
        self.position_dropdown.currentIndexChanged.connect(self.search_employees_dropdown)
        filter_layout.addWidget(self.position_dropdown)

        self.employee_search = QLineEdit()
        self.employee_search.setPlaceholderText("Search Employee Name...")
        self.employee_search.textChanged.connect(self.search_employees)  
        filter_layout.addWidget(self.employee_search)
        main_content_layout.addLayout(filter_layout)

        # Employee Table
        self.table_widget = EmployeeTableWidget(self)
        main_content_layout.addWidget(self.table_widget)

    def setup_finance_page(self):
        # Finances Page Layout
        finances_layout = QVBoxLayout(self.finance_page)
        
        # Add a hamburger button to the header
        # make this button always stay on the left side of the header
        self.hamburger_button = QPushButton()
        self.hamburger_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))
        self.hamburger_button.setFixedWidth(30)
        self.hamburger_button.setFixedHeight(30)
        self.hamburger_button.setStyleSheet("background-color: #1abc9c; color: white;")
        self.hamburger_button.clicked.connect(self.toggle_sidebar)
        self.hamburger_button.setVisible(True)  # Initially hidden
        # Add the hamburger button to the header layout
        finances_layout.addWidget(self.hamburger_button)

        # Finance Manager
        self.finance_manager = FinanceManager()
        self.finance_manager.setup_ui()
        finances_layout.addWidget(self.finance_manager)

    def add_employee(self):
        dialog = EmployeeDialog(self)
        if dialog.exec():
            data = dialog.get_employee_data()
            new_employee = Employee(
                name=data['name'],
                employee_id=data['employee_id'],
                gender=data['gender'],
                position=data['position'],
                birthday=data['birthday'],
                address=data['address'],
                phone=data['phone'],
                email=data['email']
            )
            self.table_widget.employee_manager.add_employee(new_employee)
            self.table_widget.load_employees()

    def search_employees(self, search_text):
        employees = self.table_widget.employee_manager.search_employees(search_text)
        if not employees:
            QMessageBox.information(self, "Search Result", "No matching employees found.")
            self.table_widget.load_employees([])
        else:
            self.table_widget.load_employees(employees)

    def toggle_sidebar(self):
        if self.sidebar.isVisible():
            self.sidebar.setVisible(False)
            self.hamburger_button.setVisible(True)
            self.sidebar.toggle_sidebar_button.setText("Show Sidebar")
        else:
            self.sidebar.setVisible(True)
            self.hamburger_button.setVisible(False)
            self.sidebar.toggle_sidebar_button.setText("Hide Sidebar")

#i want to add methods to switch between the pages form the sidebar
    def show_manage_employees(self):
        self.stacked_widget.setCurrentWidget(self.employee_page)

    def show_manage_finances(self):
        self.stacked_widget.setCurrentWidget(self.finance_page)

 #i wanna add a method to filter the employees by position

    def search_employees_dropdown(self):
        selected_position = self.position_dropdown.currentText().strip()

        # Check if a valid position is selected
        if not selected_position or selected_position == "All Position":
            query = self.session.query(Employee)
        else:
            query = self.session.query(Employee).filter(Employee.position == selected_position)

        try:
            # Execute the query to fetch employees
            employees = query.all()
        except Exception as e:
            # Handle any exceptions that occur during the query
            QMessageBox.critical(self, "Database Error", f"An error occurred while fetching employees:\n{str(e)}")
            employees = []
        
        # Check if any employees were found
        if not employees:
            QMessageBox.information(self, "Search Result", "No matching employees found.")
            self.table_widget.load_employees([])
        else:
            self.table_widget.load_employees(employees)


    # def closeEvent(self, event):
    #     """Handle cleanup when the main window is closed."""
    #     reply = QMessageBox.question(
    #         self,
    #         "Confirm Exit",
    #         "Are you sure you want to exit the application?",
    #         QMessageBox.Yes | QMessageBox.No
    #     )

    #     if reply == QMessageBox.Yes:
    #         # Emit signal to close all child windows
    #         self.close_all_windows_signal.emit()

    #         # Perform additional cleanup if necessary
    #         # e.g., logging out user, closing database sessions

    #         event.accept()
    #     else:
    #         event.ignore()

    # def register_child_window(self, window):
    #     """Register a child window to ensure it closes with the main window."""
    #     self.child_windows.append(window)
    #     self.close_all_windows_signal.connect(window.close)