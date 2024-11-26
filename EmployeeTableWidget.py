from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from DBModel import Employee, Session, session
from MainMethods import *
from EmployeeDialog import EmployeeDialog


# Employee Table Widget
class EmployeeTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(10)
        self.setHorizontalHeaderLabels(["Name", "Employee ID", "Gender", "Position", "Birthday", "Address", "Phone", "Email", "Edit", "Delete"])
        self.setAlternatingRowColors(True)
        self.setStyleSheet("QTableWidget { gridline-color: #bdc3c7; } QTableWidget::item { padding: 5px; }")
        self.employee_manager = EmployeeManager()
        self.load_employees()

    def load_employees(self, employees=None):
        # Clear existing rows
        self.setRowCount(0)
        
        # Fetch employees from the database
        if employees is None:
            employees = self.employee_manager.get_all_employees()
        
        for row_idx, employee in enumerate(employees):
            # Insert a new row at the current row index
            self.insertRow(row_idx)
            # Set the item at the current row index and column 0 to the employee name
            self.setItem(row_idx, 0, QTableWidgetItem(employee.name))
            # Set the item at the current row index and column 1 to the employee id
            self.setItem(row_idx, 1, QTableWidgetItem(employee.employee_id))
            # Set the item at the current row index and column 2 to the employee gender
            self.setItem(row_idx, 2, QTableWidgetItem(employee.gender))
            # Set the position item at the current row index and column 3 to the employee position
            self.setItem(row_idx, 3, QTableWidgetItem(employee.position))
            # Set the birthday item at the current row index and column 4 to the employee birthday
            self.setItem(row_idx, 4, QTableWidgetItem(str(employee.birthday)))
            # Set the address item at the current row index and column 5 to the employee address
            self.setItem(row_idx, 5, QTableWidgetItem(employee.address))
            # Set the phone item at the current row index and column 6 to the employee phone
            self.setItem(row_idx, 6, QTableWidgetItem(employee.phone))
            # Set the email item at the current row index and column 7 to the employee email
            self.setItem(row_idx, 7, QTableWidgetItem(employee.email))

            # Edit Button
            edit_button = QPushButton("Edit")
            edit_button.setStyleSheet("background-color: #000066; color: white; border-radius: 5px;")
            edit_button.clicked.connect(lambda ch, employee_id=employee.employee_id: self.edit_employee(employee_id))
            self.setCellWidget(row_idx, 8, edit_button)

            # Delete Button
            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet("background-color: #b30000; color: white; border-radius: 5px;")
            delete_button.clicked.connect(lambda ch, employee_id=employee.employee_id: self.delete_employee(employee_id))
            self.setCellWidget(row_idx, 9, delete_button)

    def edit_employee(self, employee_id):
        employee = self.employee_manager.session.query(Employee).filter(Employee.employee_id == employee_id).first()
        if employee:
            dialog = EmployeeDialog(self, employee)
            if dialog.exec():
                data = dialog.get_employee_data()
                employee.name = data['name']
                employee.gender = data['gender']
                employee.position = data['position']
                employee.birthday = data['birthday']
                employee.address = data['address']
                employee.phone = data['phone']
                employee.email = data['email']
                self.employee_manager.update_employee(employee)
                self.load_employees()

    def delete_employee(self, employee_id):
        self.employee_manager.delete_employee(employee_id)
        self.load_employees()
