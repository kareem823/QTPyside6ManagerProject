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
        self.setup_invoices_ui()

    def setup_invoices_ui(self):
        layout = QVBoxLayout(self)

        # Title
        create_invoice_label = QLabel("Create Invoice")
        create_invoice_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(create_invoice_label)

        # Instructions
        invoice_instructions_label = QLabel("Please press on one of the PDF or Word buttons to export the invoice to your device.")
        invoice_instructions_label.setStyleSheet("font-size: 12px; color: red; font-weight: italic;")
        layout.addWidget(invoice_instructions_label) 


        # Business Name
        business_name_label = QLabel(f"Business Name: {self.business_name}")
        layout.addWidget(business_name_label)

        # Invoice Number
        invoice_number_input = QLineEdit()
        invoice_number_input.setPlaceholderText("Invoice Number")
        layout.addWidget(invoice_number_input)

        # Date Inputs
        date_layout = QHBoxLayout()
        date_label = QLabel("Today's Date:")
        date_layout.addWidget(date_label)
        date_input = QDateEdit()
        date_input.setCalendarPopup(True)
        date_input.setDate(QDate.currentDate())
        date_layout.addWidget(date_input)

        #due date input
        due_date_label = QLabel("Due Date:")
        date_layout.addWidget(due_date_label)
        due_date_input = QDateEdit()
        due_date_input.setCalendarPopup(True)
        date_layout.addWidget(due_date_input)
        layout.addLayout(date_layout)

        # Invoice Items
        items_layout = QVBoxLayout()
        #create a list to hold the items for the invoice
        self.invoice_items = []

        add_item_button = QPushButton("Add Item +")
        add_item_button.setStyleSheet("background-color: green; color: white;")
        #In Python, lambda is a keyword used to create anonymous functions,
        # which are functions that are defined without a name. 
        # These functions can take any number of arguments but can only have a single expression.
        add_item_button.clicked.connect(lambda: self.add_invoice_item(items_layout))
        layout.addWidget(add_item_button)
        
        # Add items to the invoice
        layout.addLayout(items_layout)

        # Notes
        note_input = QTextEdit()
        note_input.setPlaceholderText("Notes")
        layout.addWidget(note_input)

        # Create Invoice Button
        create_invoice_button = QPushButton("Create Invoice")
        layout.addWidget(create_invoice_button)

        # Export Invoice Buttons
        export_buttons_layout = QHBoxLayout()

        self.file_exporter = FileExports(main_window=self)
        export_pdf_button = QPushButton("Export as PDF")
        export_pdf_button.setStyleSheet("background-color: #dc3545; color:white;")
        
        # #need to make a new method to export the invoice to word, and pdf
        # #this is because the curret methods export whats inside the employee list
        export_pdf_button.clicked.connect(self.file_exporter.export_invoice_pdf)
        export_buttons_layout.addWidget(export_pdf_button)

        export_word_button = QPushButton("Export as Word")
        export_word_button.setStyleSheet("background-color: #007bff; color: white;")
        export_word_button.clicked.connect(self.file_exporter.export_invoice_word)
        export_buttons_layout.addWidget(export_word_button)

        layout.addLayout(export_buttons_layout)

##########
    # i want to add an item to the invoice
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
        # remove_button = QPushButton("Remove")
        # remove_button.setStyleSheet("background-color: #dc3545; color: white;")
        # remove_button.clicked.connect(lambda: self.remove_invoice_item(item_layout, items_layout))
        # item_layout.addWidget(remove_button)
        remove_button = QPushButton("Remove")
        remove_button.setStyleSheet("background-color: #dc3545; color: white;")
        remove_button.clicked.connect(lambda: self.remove_invoice_item(item_layout, items_layout))

        items_layout.addLayout(item_layout)
        self.invoice_items.append(item_layout)


    def remove_invoice_item(self, item_layout, items_layout):
        # Remove the item layout from the list and layout
        self.invoice_items.remove(item_layout)
        QWidget().setLayout(item_layout)
        items_layout.removeItem(item_layout)


