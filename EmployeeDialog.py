from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from DBModel import Employee, Session, session
from MainMethods import *

# Dialog for adding/editing employees
class EmployeeDialog(QDialog):
    def __init__(self, parent=None, employee=None):
        super().__init__(parent)
        self.setWindowTitle("Add Employee" if employee is None else "Edit Employee")
        self.employee = employee
        self.setup_ui()

    def setup_ui(self):
        self.dialog_layout = QVBoxLayout(self)


        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.dialog_layout.addWidget(self.name_input)

        self.employee_id_input = QLineEdit()
        self.employee_id_input.setPlaceholderText("Employee ID")
        self.dialog_layout.addWidget(self.employee_id_input)

        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female"])
        self.dialog_layout.addWidget(self.gender_input)

        self.position_input = QLineEdit()
        self.position_input.setPlaceholderText("Position (e.g., Manager, Developer)")
        self.dialog_layout.addWidget(self.position_input)

        #I want to enter the birth date with the calender widget
        self.birthday_input = QDateEdit()
        self.birthday_input.setCalendarPopup(True)
        self.dialog_layout.addWidget(self.birthday_input)

        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Address")
        self.dialog_layout.addWidget(self.address_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone")
        self.dialog_layout.addWidget(self.phone_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.dialog_layout.addWidget(self.email_input)

        self.submit_button = QPushButton("Add Employee" if self.employee is None else "Save Changes")
        self.submit_button.clicked.connect(self.accept)
        self.dialog_layout.addWidget(self.submit_button)

        if self.employee:
            self.load_employee_data()

    def load_employee_data(self):
        self.name_input.setText(self.employee.name)
        self.employee_id_input.setText(self.employee.employee_id)
        self.employee_id_input.setDisabled(True)  # Employee ID should not be changed
        self.gender_input.setCurrentText(self.employee.gender)
        self.position_input.setText(self.employee.position)
        self.birthday_input.setDate(self.employee.birthday)
        self.address_input.setText(self.employee.address)
        self.phone_input.setText(self.employee.phone)
        self.email_input.setText(self.employee.email)

    # Get employee data from the dialog
    def get_employee_data(self):
        # Get employee data from the dialog
        data = {
            #get employee name from the name input
            'name': self.name_input.text(),
            #get employee id from the employee id input
            'employee_id': self.employee_id_input.text(),
            #get employee gender from the gender input
            'gender': self.gender_input.currentText(),
            #get employee position from the position input
            'position': self.position_input.text(),
            #get employee birthday from the birthday input
            'birthday': self.birthday_input.date().toPython(),
            #get employee address from the address input
            'address': self.address_input.text(),
            'phone': self.phone_input.text(),
            'email': self.email_input.text()
        }
        return data
