from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from EmployeeEditorPage.MainMethods import MainMethods

#todo
# need to reject nulls from the db
#need to redo rest of invoice code
#need to add delete business functionality

if __name__ == '__main__':
    # PySide6 Application
    app = QApplication(sys.argv)
    window = MainMethods()
    window.show()
    sys.exit(app.exec())
