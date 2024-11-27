from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys
from sqlalchemy import distinct
from EmployeeEditorPage.FileExports import FileExports

class InvoicePage(QWidget):
    def __init__(self, business_name):
        super().__init__()
        self.setWindowTitle("Create Invoice")
        self.setGeometry(100, 100, 600, 400)
        self.business_name = business_name
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Title
        create_invoice_label = QLabel("Create Invoice")
        create_invoice_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(create_invoice_label)

        # Instructions
        invoice_instructions_label = QLabel("Please press on one of the PDF or Word buttons to export the invoice to your device.")
        invoice_instructions_label.setStyleSheet("font-size: 12px; color: red; font-weight: italic;")
        layout.addWidget(invoice_instructions_label) 


        ########################################################################
        # Business Name
        business_name_label = QLabel(f"Business Name: {self.business_name}")
        layout.addWidget(business_name_label)

        # Invoice Number
        invoice_number_input = QLineEdit()
        invoice_number_input.setPlaceholderText("Invoice Number")
        layout.addWidget(invoice_number_input)

        # Date Inputs
        date_layout = QHBoxLayout()
        date_label = QLabel("Date:")
        date_layout.addWidget(date_label)
        date_input = QDateEdit()
        date_input.setCalendarPopup(True)
        date_layout.addWidget(date_input)

        due_date_label = QLabel("Due Date:")
        date_layout.addWidget(due_date_label)
        due_date_input = QDateEdit()
        due_date_input.setCalendarPopup(True)
        date_layout.addWidget(due_date_input)
        layout.addLayout(date_layout)

        # Invoice Items
        items_layout = QVBoxLayout()
        self.item_list = []

        add_item_button = QPushButton("Add Item")
        add_item_button.clicked.connect(lambda: self.add_invoice_item(items_layout))
        layout.addWidget(add_item_button)
        layout.addLayout(items_layout)

        # Notes
        notes_input = QTextEdit()
        notes_input.setPlaceholderText("Notes")
        layout.addWidget(notes_input)

        # Create Invoice Button
        create_invoice_button = QPushButton("Create Invoice")
        layout.addWidget(create_invoice_button)

        # Export Invoice Buttons
        export_buttons_layout = QHBoxLayout()

        self.file_exporter = FileExports(main_window=self)
        export_pdf_button = QPushButton("Export as PDF")
        export_pdf_button.setStyleSheet("background-color: #dc3545; color: white;")
        #need to make a new method to export the invoice to word, and pdf
        #this is because the curret methods export whats inside the employee list
        export_pdf_button.clicked.connect(self.file_exporter.export_pdf)
        export_buttons_layout.addWidget(export_pdf_button)

        export_excel_button = QPushButton("Export as Excel")
        export_excel_button.setStyleSheet("background-color: #007bff; color: white;")
        export_excel_button.clicked.connect(self.file_exporter.export_excel)
        export_buttons_layout.addWidget(export_excel_button)

        layout.addLayout(export_buttons_layout)

    def add_invoice_item(self, items_layout):
        item_layout = QHBoxLayout()

        # Item Description
        item_description = QLineEdit()
        item_description.setPlaceholderText("Description")
        item_layout.addWidget(item_description)

        # Quantity
        quantity_input = QSpinBox()
        item_layout.addWidget(quantity_input)

        # Price
        price_input = QDoubleSpinBox()
        item_layout.addWidget(price_input)

        # Remove Item from invoice Button
        remove_button = QPushButton("Remove")
        remove_button.setStyleSheet("background-color: #dc3545; color: white;")
        remove_button.clicked.connect(lambda: self.remove_invoice_item(item_layout, items_layout))
        item_layout.addWidget(remove_button)

        items_layout.addLayout(item_layout)
        self.item_list.append(item_layout)

    def remove_invoice_item(self, item_layout, items_layout):
        # Remove the item layout from the list and layout
        self.item_list.remove(item_layout)
        QWidget().setLayout(item_layout)
        items_layout.removeItem(item_layout)


