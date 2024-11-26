from PySide6.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PySide6.QtGui import *
from PySide6.QtCore import *
from sqlalchemy.orm import sessionmaker
from DBModel import Employee  # Ensure this imports your Employee model
from EmployeeManager import EmployeeManager  # Import your EmployeeManager class
import pandas as pd
#import plotly and fpdf
from fpdf import FPDF
import plotly.express as px
#i want to import an excel library
import xlsxwriter
from EmployeeManager import EmployeeManager  # Import your EmployeeManager class


class FileExports(QMainWindow):
    def __init__(self, main_window):
        super(FileExports, self).__init__()
        self.main_window = main_window
        # Initialize the EmployeeManager (ensure it's correctly imported)
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
            "PDF Files (*.pdf);;All Files (*)"
        )    

        if not file_path:
            QMessageBox.warning(self, "Warning", "Export cancelled.")
            return

        # Retrieve all employees from the database
        employees = self.employee_manager.get_all_employees()
        
        # Initialize QPdfWriter
        pdf = QPdfWriter(file_path)   
        pdf.setPageSize(QPageSize.A4)
        pdf.setPageMargins(QMarginsF(15, 15, 15, 15))

        painter = QPainter()
        if not painter.begin(pdf):
            QMessageBox.critical(self, "Error", "Failed to open file for writing.")
            return

        try:
            # Set up font and metrics
            font = QFont("Arial", 10)
            painter.setFont(font)
            metrics = painter.fontMetrics()
            line_height = metrics.height() + 10
            column_widths = [60, 100, 60, 100, 80, 100, 100, 150]  # Define column widths for better spacing
            
            # Define table properties
            margin = 40
            current_y = margin
            current_x = margin

            # Draw table headers with borders
            pen = QPen(Qt.black)
            pen.setWidth(1)
            painter.setPen(pen)
            
            headers = ["Employee ID", "Name", "Gender", "Position", "Birthday", "Phone", "Address", "Email"]
            for i, header in enumerate(headers):
                painter.drawRect(current_x, current_y, column_widths[i], line_height)
                painter.drawText(current_x + 5, current_y + line_height - 5, header)
                current_x += column_widths[i]
            
            current_y += line_height

            # Write employee data with borders
            for employee in employees:
                current_x = margin
                data = [
                    employee.employee_id,
                    employee.name,
                    employee.gender,
                    employee.position,
                    employee.birthday.strftime("%Y-%m-%d") if employee.birthday else "",
                    employee.phone,
                    employee.address,
                    employee.email
                ]

                for i, value in enumerate(data):
                    painter.drawRect(current_x, current_y, column_widths[i], line_height)
                    painter.drawText(current_x + 5, current_y + line_height - 5, str(value))
                    current_x += column_widths[i]
                
                current_y += line_height
                
                # If current_y exceeds page height, add a new page
                if current_y > pdf.height() - margin:
                    pdf.newPage()
                    current_y = margin
                    
                    # Re-draw headers on the new page
                    current_x = margin
                    for i, header in enumerate(headers):
                        painter.drawRect(current_x, current_y, column_widths[i], line_height)
                        painter.drawText(current_x + 5, current_y + line_height - 5, header)
                        current_x += column_widths[i]
                    current_y += line_height
                    
            painter.end()
            QMessageBox.information(self, "Success", f"PDF exported successfully to {file_path}")
        
        except Exception as e:
            painter.end()
            QMessageBox.critical(self, "Error", f"An error occurred while exporting PDF:\n{str(e)}")
