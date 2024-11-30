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

from PySide6.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle


'''
make a def for creating a qr code for each pdf we make.
'''

class FileExports(QMainWindow):
    # Define headers as a class attribute
    HEADERS = ["Employee ID", "Name", "Gender", "Position", "Birthday", "Phone", "Address", "Email"]

    def __init__(self, main_window):
        super(FileExports, self).__init__()
        self.main_window = main_window
        self.employee_manager = EmployeeManager()



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

        try:
            # Initialize the excel writer
            workbook = xlsxwriter.Workbook(file_path)
            worksheet = workbook.add_worksheet()
            
            # Write the headers
            headers = self.HEADERS
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
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export Excel.\nError: {str(e)}")


    def export_pdf(self):
        # Open a file dialog to select the save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF File",
            "",
            "PDF Files (*.pdf);; All Files (*)"
        )

        if not file_path:
            QMessageBox.warning(self, "Warning", "Export cancelled.")
            return

        try:
            # Create a PDF document
            doc = SimpleDocTemplate(file_path, pagesize=letter)

            # Define headers excluding 'id' and in the desired order
            headers = self.HEADERS

            # Initialize data with headers
            data = [headers]

            # Retrieve employee data
            employees = self.employee_manager.get_all_employees()
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

            # Calculate column widths
            total_width = doc.width
            col_widths = [
                total_width * 0.12,  # Employee ID
                total_width * 0.18,  # Name
                total_width * 0.10,  # Gender
                total_width * 0.15,  # Position
                total_width * 0.12,  # Birthday
                total_width * 0.12,  # Phone
                total_width * 0.15,  # Address
                total_width * 0.16   # Email
            ]

            # Define helper function
            def get_fit_font_size(text, font_name, max_width, max_font_size, min_font_size=6, step=0.5):
                font_size = max_font_size
                while font_size >= min_font_size:
                    text_width = stringWidth(text, font_name, font_size)
                    if text_width <= max_width:
                        return font_size
                    font_size -= step
                return min_font_size

            # Prepare styles
            header_style = ParagraphStyle(
                name='HeaderStyle',
                fontName='Helvetica-Bold',
                fontSize=10,
                alignment=1,  # Center alignment
                textColor=colors.white
            )
            cell_style = ParagraphStyle(
                name='CellStyle',
                fontName='Helvetica',
                fontSize=10,
                alignment=1,  # Center alignment
            )

            # Adjust headers and data with Paragraphs
            styled_data = []
            for row_idx, row in enumerate(data):
                styled_row = []
                for col_idx, cell in enumerate(row):
                    if row_idx == 0:
                        # Header row
                        para = Paragraph(cell, header_style)
                    else:
                        # Data rows
                        available_width = col_widths[col_idx] - 4  # Subtracting small padding
                        font_size = get_fit_font_size(
                            text=str(cell),
                            font_name=cell_style.fontName,
                            max_width=available_width,
                            max_font_size=cell_style.fontSize
                        )
                        dynamic_style = ParagraphStyle(
                            name='DynamicCellStyle',
                            fontName=cell_style.fontName,
                            fontSize=font_size,
                            alignment=cell_style.alignment,
                        )
                        para = Paragraph(str(cell), dynamic_style)
                    styled_row.append(para)
                styled_data.append(styled_row)

            # Create the table with styled data
            pdf_table = Table(styled_data, colWidths=col_widths, repeatRows=1)

            # Apply style to the table
            pdf_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.gray),  # Header row background
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header row text color
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for all cells
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header row font
                ('FONTSIZE', (0, 0), (-1, -1), 10),  # Default font size
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header row padding
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Grid lines
            ]))

            # Add alternating row colors for better readability
            for i in range(1, len(styled_data)):
                if i % 2 == 0:
                    bg_color = colors.whitesmoke
                else:
                    bg_color = colors.lightgrey
                pdf_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, i), (-1, i), bg_color)
                ]))

            # Build the PDF
            elements = [pdf_table]
            doc.build(elements)

            QMessageBox.information(self, "Success", "PDF exported successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export PDF.\nError: {str(e)}")

    