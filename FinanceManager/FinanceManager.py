from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys
from sqlalchemy import distinct
from FinanceManager.InvoicesPage import InvoicePage
from CompanyListDB import CompaniesListDB, clBase, clengine, clSession
# from SideBar import Sidebar

class FinanceManager(QMainWindow):

    def __init__(self):
        """
        Constructor for the FinanceManager window. Sets up the window, sidebar, and
        connects to the database. It also populates the list of companies in the
        sidebar with data from the database.

        :return: None
        """
        super().__init__()
        self.setWindowTitle("Manage Finances")
        self.setGeometry(100, 100, 800, 600)
        # self.invoice_page = InvoicePage()

        #set the comapny name
        #self.company_name = "Company"

        # Connect to the database
        self.session = clSession()
        self.companies_list = self.session.query(CompaniesListDB).all()
        self.business_list_widget = QListWidget()
        self.business_list_widget.addItems([company.company_name for company in self.companies_list])


        self.setup_ui()

    def setup_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        qvLayout = QVBoxLayout(central_widget)

        # Manage Finances Title
        manage_finance_label = QLabel("Manage Finances")
        manage_finance_label.setStyleSheet('''font-family: Garamond; font-size: 24px; font-weight:bold;''')
        qvLayout.addWidget(manage_finance_label)

        # Instructions
        invoice_instructions_label = QLabel("Fill out the form below and press on the business name to create an invoice.")
        invoice_instructions_label.setStyleSheet("font-size: 12px; font-weight: italic;")
        qvLayout.addWidget(invoice_instructions_label) 

        # Input for Business Name
        business_name_label = QLabel("Add Business:")
        qvLayout.addWidget(business_name_label)
        self.business_name_input = QLineEdit()
        #set the initial value to null
        self.business_name_input.setText(None)
        self.business_name_input.setPlaceholderText("Enter business name")
        qvLayout.addWidget(self.business_name_input)

        # a qDate widget for the company date join
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        qvLayout.addWidget(self.date_input)

        # Button to add a business
        add_business_button = QPushButton("Add Business")
        add_business_button.clicked.connect(self.add_business)
        #add_business_button.clicked.connect(self.add_company_to_db(self.business_name_input.text(), date_input.date().toPython()))
        qvLayout.addWidget(add_business_button)   

        # Business List
        self.business_list_widget = QListWidget()
        self.business_list_widget.itemClicked.connect(self.create_invoice_page)
        qvLayout.addWidget(self.business_list_widget)

        #delete a business from the database
        delete_business_button = QPushButton("Delete Selected Business")
        #when the button is clicked i want to call the delte function
        delete_business_button.clicked.connect(self.delete_company)
        #add button to layout
        qvLayout.addWidget(delete_business_button)

        #load all businesses from the database to the list widget
        self.business_list_widget.addItems([company.company_name for company in self.companies_list])

    def add_business(self):
        """
        Add the business name to the list widget and the database.
        If the user didn't enter a business name, display a warning message.
        :return: None
        """
        business_name = self.business_name_input.text().strip()
        date = self.date_input.date().toPython()
        if not business_name:
            QMessageBox.warning(self, "Error", "Please enter a business name")
            return

        item = QListWidgetItem(business_name)
        self.business_list_widget.addItem(item)
        self.business_name_input.clear()

        #add the company to the database
        self.add_company_to_db(business_name, date)
        
    def add_company_to_db(self, cname, cdate):
        #if the cname and cdate are null then i want to give an error message and return
        if (cname is None and cdate is None):
                QMessageBox.warning(self, "Error", "Please enter a business name and date")
                return
        #i want to add the user input to the database
        #create a new session
        session = clSession()
        
        #create a company instance
        new_company = CompaniesListDB(
            company_name = cname,
            business_start_date = cdate
        )        
            #add the company to the database
        session.add(new_company)

        try:
            session.commit()
            print("Success! Company added to database successfully!")
        except Exception as e:
            print(f"Error adding company to database: {e}")
            session.rollback()
            QMessageBox.critical(self, "Database Error", "Failed to add the company to the database.")

        finally:
            session.close()

        
    def create_invoice_page(self, item):
        self.invoice_page = InvoicePage(business_name=item.text())
        self.invoice_page.show()

    #delete a business from the database and list            
    def delete_company(self):
        """
        Delete the selected business from the list widget and the database.
        If no business is selected, display a warning message.
        :return: None
        """

        # Get the currently selected item from the business list widget
        selected_item = self.business_list_widget.currentItem()
        
        # Check if an item is selected; if not, show a warning message
        if selected_item is None:
            QMessageBox.warning(self, "Error", "Please select a business to delete")
            return  # Exit the method if no item is selected
        
        # Get the company name from the selected item
        business_name = selected_item.text()

        # Prompt the user for confirmation before deletion
        reply = QMessageBox.question(self, 
                                    "Confirm Deletion?",
                                    f"Are you sure you want to delete {business_name}?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        # If the user confirms the deletion (reply is Yes)
        if reply == QMessageBox.Yes:
            # Remove the item from the list widget
            self.business_list_widget.takeItem(self.business_list_widget.row(selected_item))

            # Create a new session to interact with the database
            session = clSession()
            try:
                # Find the company in the database using the company name
                company_to_delete = session.query(CompaniesListDB).filter_by(company_name=business_name).first()
                
                # If the company is found in the database, proceed to delete it
                if company_to_delete:
                    session.delete(company_to_delete)  # Delete the company from the session
                    session.commit()  # Commit the changes to the database
                    print("Success! Company deleted from database successfully!")  # Log success message
                else:
                    print("Company not found in database.")  # Log if the company was not found
            except Exception as e:
                # Handle any exceptions that occur during the deletion process
                print(f"Error deleting company from database: {e}")  # Log the error message
                session.rollback()  # Rollback the session to maintain database integrity
                QMessageBox.critical(self, "Database Error", "Failed to delete the company from the database.")  # Show error message to the user

            finally:
                session.close()  # Ensure the session is closed after the operation
