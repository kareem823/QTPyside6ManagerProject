from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker

# Setting up SQLAlchemy for database management
clBase = declarative_base()
clengine = create_engine('sqlite:///companies_list.db')

#create the session object for database operations
clSession = sessionmaker(bind=clengine)
clsession = clSession()

#define the company list class
class CompaniesListDB(clBase):
    #set the table name
    __tablename__ = 'companies_list'

    #define the columns
    company_id = Column(Integer, primary_key=True)
    company_name = Column(String, nullable=False)
    business_start_date = Column(Date, nullable=False)

#create the table if it doesn't exist
clBase.metadata.create_all(clengine)