import webbrowser
from PySide6.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PySide6.QtGui import *
from PySide6.QtCore import *
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
import sys
from EmployeeEditorPage.EmployeeManager import EmployeeManager  # Import your EmployeeManager class

sys.path.insert(0, './')

from DBModel import Employee, engine, Session  # Ensure this imports your Employee model
# from EmployeeManager import EmployeeManager  # Import your EmployeeManager class
import pandas as pd
#import plotly and fpdf
from fpdf import FPDF
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib import *
#i want to import an excel library
import xlsxwriter


class FileExports(QMainWindow):
    def __init__(self, main_window):
        super(FileExports, self).__init__()
        self.main_window = main_window

        self.employee_manager = EmployeeManager()


    # Export data as Excel file (implementation can be added later)
    def export_excel(self):

        # Open a file dialog to select the save location
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save Excel File", 
            "", 
            "Excel Files (*.xlsx);;All Files (*)"
        )    

        if not file_path:
            QMessageBox.warning(self, "Warning", "Export cancelled.")
            return

        # Initialize the excel writer
        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet()
        
        # Write the headers
        headers = ["Employee ID", "Name", "Gender", "Position", "Birthday", "Phone", "Address", "Email"]
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)
        
        # Write the data
        employees = self.employee_manager.get_all_employees()
        for row_num, employee in enumerate(employees, 1):
            worksheet.write(row_num, 0, employee.employee_id)
            worksheet.write(row_num, 1, employee.name)
            worksheet.write(row_num, 2, employee.gender)
            worksheet.write(row_num, 3, employee.position)
            worksheet.write(row_num, 4, employee.birthday.strftime("%Y-%m-%d") if employee.birthday else "")
            worksheet.write(row_num, 5, employee.phone)
            worksheet.write(row_num, 6, employee.address)
            worksheet.write(row_num, 7, employee.email)
        
        workbook.close()
        QMessageBox.information(self, "Success", "Excel exported successfully.")


    # Export data as PDF file
    def export_pdf(self):

        # Open a file dialog to select the save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF File",
            "",
            "PDF Files (*.pdf);; All Files (*)"
        )

        if file_path:
            #create a pdf document
            doc = SimpleDocTemplate(file_path, page_size=letter)

        # Use SQLAlchemy's inspector to get column names
        inspector = inspect(engine)
        columns = inspector.get_columns('employees')
        headers = [col['name'] for col in columns]

        # Retrieve employee data
        employees = self.employee_manager.get_all_employees()
        data = [headers]  # Initialize data with headers

        for employee in employees:
            row = [
                employee.employee_id,
                employee.name,
                employee.gender,
                employee.position,
                employee.birthday.strftime("%Y-%m-%d") if employee.birthday else "",
                employee.phone,
                employee.address,
                employee.email
            ]
            data.append(row)

            pdf_table = Table(data)

            # apply style to the table
            pdf_table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                           ('FONTNAME', (0,0), (-1, -1), 'Helvetica'),
                                           ('FONTSIZE', (0,0), (-1, -1), 12),
                                           ('BOTTOMPADDING', (0,0), (-1, -1), 12),
                                           ('GRID', (0,0), (-1, -1), 1, colors.black),
                                           ]))
            #build the document
            elements = [pdf_table]
            doc.build(elements)

        QMessageBox.information(self, "Success", "PDF saved successfully!")

            
            

