from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from FinanceManager.InvoiceExporter import InvoiceExporter  # Ensure correct import path
from datetime import datetime

class InvoicePage(QWidget):
    def __init__(self, business_name):
        super().__init__()
        self.setWindowTitle("Create Invoice")
        self.setGeometry(100, 100, 600, 600)  # Increased height for better UI
        self.business_name = business_name
        self.invoice_exporter = InvoiceExporter(parent=self)  # Initialize InvoiceExporter **before** setting up UI
        self.setup_invoices_ui()

    def setup_invoices_ui(self):
        layout = QVBoxLayout(self)

        # Title
        create_invoice_label = QLabel("Create Invoice")
        create_invoice_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(create_invoice_label)

        # Instructions
        invoice_instructions_label = QLabel("Please press one of the PDF or Word buttons to export the invoice to your device.")
        invoice_instructions_label.setStyleSheet("font-size: 12px; color: red; font-weight: italic;")
        layout.addWidget(invoice_instructions_label) 

        # Business Name
        business_name_label = QLabel(f"Business Name: {self.business_name}")
        business_name_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(business_name_label)

        # Invoice Number
        invoice_number_input = QLineEdit()
        invoice_number_input.setPlaceholderText("Invoice Number")
        invoice_number_input.setObjectName("invoice_number")
        layout.addWidget(invoice_number_input)

        # Customer Name
        customer_name_input = QLineEdit()
        customer_name_input.setPlaceholderText("Customer Name")
        customer_name_input.setObjectName("customer_name")
        layout.addWidget(customer_name_input)

        # Customer Email
        customer_email_input = QLineEdit()
        customer_email_input.setPlaceholderText("Customer Email")
        customer_email_input.setObjectName("customer_email")
        layout.addWidget(customer_email_input)

        # Customer Phone
        customer_phone_input = QLineEdit()
        customer_phone_input.setPlaceholderText("Customer Phone")
        customer_phone_input.setObjectName("customer_phone")
        layout.addWidget(customer_phone_input)

        # Customer Address
        customer_address_input = QLineEdit()
        customer_address_input.setPlaceholderText("Customer Address")
        customer_address_input.setObjectName("customer_address")
        layout.addWidget(customer_address_input)

        # Date Inputs
        date_layout = QHBoxLayout()
        date_label = QLabel("Today's Date:")
        date_layout.addWidget(date_label)
        date_input = QDateEdit()
        date_input.setCalendarPopup(True)
        date_input.setDate(QDate.currentDate())
        date_input.setObjectName("invoice_date")
        date_layout.addWidget(date_input)

        # Due Date Input
        due_date_label = QLabel("Due Date:")
        date_layout.addWidget(due_date_label)
        due_date_input = QDateEdit()
        due_date_input.setCalendarPopup(True)
        due_date_input.setDate(QDate.currentDate().addDays(30))  # Default due date 30 days later
        due_date_input.setObjectName("due_date")
        date_layout.addWidget(due_date_input)
        layout.addLayout(date_layout)

        # Invoice Items
        items_layout = QVBoxLayout()
        self.invoice_items = []  # List to hold item layouts

        add_item_button = QPushButton("Add Item +")
        add_item_button.setStyleSheet("background-color: green; color: white;")
        add_item_button.clicked.connect(lambda: self.add_invoice_item(items_layout))
        layout.addWidget(add_item_button)
        
        # Add items to the invoice
        layout.addLayout(items_layout)

        # Notes
        note_input = QTextEdit()
        note_input.setPlaceholderText("Notes")
        note_input.setObjectName("notes")
        layout.addWidget(note_input)

        # Company Footer
        company_footer_input = QTextEdit()
        company_footer_input.setPlaceholderText("Company Footer")
        company_footer_input.setObjectName("company_footer")
        layout.addWidget(company_footer_input)

        # Export Invoice Buttons
        export_buttons_layout = QHBoxLayout()

        export_pdf_button = QPushButton("Export as PDF")
        export_pdf_button.setStyleSheet("background-color: #dc3545; color:white;")
        export_pdf_button.clicked.connect(self.handle_export_pdf)  # Connect to handler method
        export_buttons_layout.addWidget(export_pdf_button)

        export_word_button = QPushButton("Export as Word")
        export_word_button.setStyleSheet("background-color: #007bff; color: white;")
        export_word_button.clicked.connect(self.handle_export_word)  # Connect to handler method
        export_buttons_layout.addWidget(export_word_button)

        layout.addLayout(export_buttons_layout)

    # Method to add an invoice item
    def add_invoice_item(self, items_layout):
        item_layout = QHBoxLayout()

        # Item Description
        item_description = QLineEdit()
        item_description.setPlaceholderText("Description")
        item_description.setObjectName("item_description")
        item_layout.addWidget(item_description)

        # Quantity
        quantity_input = QSpinBox()
        quantity_input.setMinimum(1)
        quantity_input.setMaximum(1000)
        quantity_input.setValue(1)  # Set default value to 1
        quantity_input.setObjectName("quantity_input")
        item_layout.addWidget(quantity_input)

        # Price
        price_input = QDoubleSpinBox()
        price_input.setMinimum(0.01)
        price_input.setDecimals(2)
        price_input.setValue(0.00)
        price_input.setObjectName("price_input")
        item_layout.addWidget(price_input)

        # Remove Button
        remove_button = QPushButton("Remove")
        remove_button.setStyleSheet("background-color: #dc3545; color: white;")
        remove_button.clicked.connect(lambda: self.remove_invoice_item(item_layout, items_layout))
        item_layout.addWidget(remove_button)

        # Add the item layout to the invoice items list and to the GUI
        items_layout.addLayout(item_layout)
        self.invoice_items.append(item_layout)

    # Method to remove an invoice item
    def remove_invoice_item(self, item_layout, items_layout):
        try:
            # Remove the item layout from the list
            self.invoice_items.remove(item_layout)
        except ValueError:
            QMessageBox.warning(self, "Removal Error", "Attempted to remove an item that does not exist.")
            return

        # Remove all widgets from the layout
        while item_layout.count():
            child = item_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Remove the layout from the parent layout
        items_layout.removeItem(item_layout)

    # Method for handling the export to PDF
    def handle_export_pdf(self):
        invoice_data = self.collect_invoice_data()
        if invoice_data:
            self.invoice_exporter.export_invoice_pdf(invoice_data)

    # Method for handling the export to Word
    def handle_export_word(self):
        invoice_data = self.collect_invoice_data()
        if invoice_data:
            self.invoice_exporter.export_invoice_word(invoice_data)

    # Method to collect all invoice data from the GUI
    def collect_invoice_data(self):
        # Retrieve inputs with correct object names
        invoice_number_widget = self.findChild(QLineEdit, "invoice_number")
        customer_name_widget = self.findChild(QLineEdit, "customer_name")
        invoice_date_widget = self.findChild(QDateEdit, "invoice_date")
        due_date_widget = self.findChild(QDateEdit, "due_date")
        notes_widget = self.findChild(QTextEdit, "notes")

        # Ensure all widgets are found
        if not all([invoice_number_widget, customer_name_widget, invoice_date_widget, due_date_widget, notes_widget]):
            QMessageBox.warning(self, "Error", "One or more input fields are missing.")
            return None

        invoice_number = invoice_number_widget.text().strip()
        customer_name = customer_name_widget.text().strip()
        invoice_date = invoice_date_widget.date().toString("yyyy-MM-dd")
        due_date = due_date_widget.date().toString("yyyy-MM-dd")
        notes = notes_widget.toPlainText().strip()

        # Validation
        if not invoice_number:
            QMessageBox.warning(self, "Input Error", "Please enter an invoice number.")
            return None

        if not customer_name:
            QMessageBox.warning(self, "Input Error", "Please enter a customer name.")
            return None

        if not self.invoice_items:
            QMessageBox.warning(self, "Input Error", "Please add at least one invoice item.")
            return None

        items = []
        for index, item_layout in enumerate(self.invoice_items, start=1):
            # Access widgets by their position in the layout
            description_widget = item_layout.itemAt(0).widget()
            quantity_widget = item_layout.itemAt(1).widget()
            price_widget = item_layout.itemAt(2).widget()

            # Check if widgets exist
            if not all([description_widget, quantity_widget, price_widget]):
                QMessageBox.warning(self, "Input Error", f"One or more fields are missing in item {index}.")
                return None

            description = description_widget.text().strip()
            quantity = quantity_widget.value()
            price = price_widget.value()

            # Validation for each item
            if not description:
                QMessageBox.warning(self, "Input Error", f"Please enter a description for item {index}.")
                return None

            if quantity <= 0:
                QMessageBox.warning(self, "Input Error", f"Quantity for item {index} must be greater than zero.")
                return None

            if price <= 0:
                QMessageBox.warning(self, "Input Error", f"Price for item {index} must be greater than zero.")
                return None

            items.append({
                "item_description": description,
                "quantity": quantity,
                "price": price
            })

        # Create a dictionary to hold the invoice data
        invoice_data = {
            "business_name": self.business_name,
            "invoice_number": invoice_number,
            "customer_name": customer_name,
            "invoice_date": invoice_date,
            "due_invoice_date": due_date,
            "notes": notes,
            "invoice_items": items
        }         
        
        return invoice_data
