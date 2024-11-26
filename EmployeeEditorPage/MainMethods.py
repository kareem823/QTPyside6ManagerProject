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

# Main Window Class
class MainMethods(QMainWindow):
    def __init__(self):
        super().__init__()

        # make the global variable for the company name
        self.company_name = "Company"
        # make the global variable for the username
        self.username = "User"

        self.setWindowTitle("Employee Management System")
        self.setGeometry(100, 100, 1300, 700)
        self.setup_ui()

    def setup_ui(self):
        # Main window structure
        central_widget = QWidget()
        # Set the central widget as the main widget of the window
        self.setCentralWidget(central_widget)
        # Create a horizontal layout for the central widget
        main_layout = QHBoxLayout(central_widget)

        # Left Sidebar (Collapsible)
        self.sidebar = Sidebar(self)
        main_layout.addWidget(self.sidebar)

        # Main Content Area
        main_content = QWidget()
        # Create a vertical layout for the main content
        main_content_layout = QVBoxLayout(main_content)

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
        self.hamburger_button.setVisible(False)  # Initially hidden
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
        employee_info_label.setStyleSheet("font-family: Georgia, sans-serif; font-size: 20px; font-weight: bold; padding: 10px 0;")
        main_content_layout.addWidget(employee_info_label)


        # Ensure the icon files are in the same directory as this script or provide the correct path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        excel_icon_path = os.path.join(current_dir, 'excel_icon.png')
        pdf_icon_path = os.path.join(current_dir, 'pdf_icon.png')

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
        excel_icon = QIcon(excel_icon_path)
        export_excel_button.setIcon(excel_icon)
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
        pdf_icon = QIcon(pdf_icon_path)
        export_pdf_button.setIcon(pdf_icon)
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
        # Add positions to the dropdown from the Employee database
        self.session = Session()
        # Query distinct positions from the database
        distinct_positions = self.session.query(distinct(Employee.position)).all()

        # Extract positions from query result
        positions = [position[0] for position in distinct_positions]

        # Add positions to the dropdown
        self.position_dropdown.addItems(["All Position"] + positions)

        self.position_dropdown.currentIndexChanged.connect(self.search_employees)

        filter_layout.addWidget(self.position_dropdown)



        self.employee_search = QLineEdit()
        self.employee_search.setPlaceholderText("Search Employee Name...")
        self.employee_search.textChanged.connect(self.search_employees)  
        filter_layout.addWidget(self.employee_search)
        main_content_layout.addLayout(filter_layout)

        # Employee Table
        self.table_widget = EmployeeTableWidget(self)
        main_content_layout.addWidget(self.table_widget)

        # Add main content to the main layout
        main_layout.addWidget(main_content, stretch=1)

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
