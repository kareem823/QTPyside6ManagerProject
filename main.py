from PySide6.QtWidgets import QApplication
import sys
from EmployeeEditorPage.MainMethods import MainMethods
from Authentication.SignInWindow import SignInWindow
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from EmployeeEditorPage.MainMethods import MainMethods
from Authentication.SignInWindow import SignInWindow  


#todo
#save invoice file buttons
#add the notes app to the sidebar

'''
fix the login, signup and forgot password window close mechanisms
'''

if __name__ == '__main__':
    # PySide6 Application
    app = QApplication(sys.argv)

    # #setup the authentication window
    # signin_window = SignInWindow()
    # signin_window.show()

    main_window = MainMethods()
    main_window.show()    
    #show the main window if the authentication is successful
    # signin_window.login_successful.connect(lambda: (signin_window.close(), main_window.show()))

    sys.exit(app.exec())
    