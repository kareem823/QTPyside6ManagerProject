from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys
from sqlalchemy import distinct
from EmployeeEditorPage.FileExports import FileExports

class FinanceManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Finances")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Manage Finances Title
        manage_finances_label = QLabel("Manage Finances")
        manage_finances_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(manage_finances_label)

        # Input for Business Name
        self.business_name_input = QLineEdit()
        self.business_name_input.setPlaceholderText("Enter business name")
        layout.addWidget(self.business_name_input)

        # Button to add a business
        add_business_button = QPushButton("Add Business")
        add_business_button.clicked.connect(self.add_business)
        layout.addWidget(add_business_button)

        # Business List
        self.business_list_widget = QListWidget()
        self.business_list_widget.itemClicked.connect(self.create_invoice_page)
        layout.addWidget(self.business_list_widget)

    def add_business(self):
        business_name = self.business_name_input.text()
        if business_name:
            item = QListWidgetItem(business_name)
            self.business_list_widget.addItem(item)
            self.business_name_input.clear()

    def create_invoice_page(self, item):
        self.invoice_page = InvoicePage(business_name=item.text())
        self.invoice_page.show()

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

        self.file_exporter = FileExports()
        export_pdf_button = QPushButton("Export as PDF")
        export_pdf_button.setStyleSheet("background-color: #dc3545; color: white;")
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

        # Remove Item Button
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    finance_manager = FinanceManager()
    finance_manager.show()
    sys.exit(app.exec())
