from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from DBModel import Employee, Session, session
from EmployeeEditorPage.MainMethods import *

# Employee Manager for database operations
class EmployeeManager:
    def __init__(self):
        self.session = Session()

    # Add employee to the database
    def add_employee(self, employee):
        self.session.add(employee)
        self.session.commit()

    # Get all employees from the database
    def get_all_employees(self):
        #the query() method is used to query the database and retrieve all employees
        #the all() method is used to retrieve all the results from the query
        return self.session.query(Employee).all()

    # Delete employee from the database
    def delete_employee(self, employee_id):
        #the query() method is used to query the database and retrieve the employee with the given employee_id
        #the filter() method is used to filter the results based on the employee_id
        #the first() method is used to retrieve the first result from the query
        employee = self.session.query(Employee).filter(Employee.employee_id == employee_id).first()
        if employee:
            self.session.delete(employee)
            self.session.commit()

    # Update employee in the database
    def update_employee(self, employee):
        self.session.commit()

    # Search employees in the database
    def search_employees(self, search_text):
        search_pattern = f"%{search_text}%"
        employees = self.session.query(Employee).filter(
            Employee.name.like(search_pattern) |
            Employee.employee_id.like(search_pattern) |
            Employee.position.like(search_pattern) |
            Employee.address.like(search_pattern) |
            Employee.email.like(search_pattern) |
            Employee.phone.like(search_pattern)
        ).all()
    
        #if the employee is not found, return all employees

        # If no employees found, return all employees
        if not employees:
            return self.get_all_employees()
        
        return employees

        

