from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker

# Setting up SQLAlchemy for database management
Base = declarative_base()
engine = create_engine('sqlite:///employee_management.db')
Session = sessionmaker(bind=engine)
session = Session()

# Defining the Employee model
class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    employee_id = Column(String, unique=True, nullable=False)
    gender = Column(String, nullable=False)
    position = Column(String, nullable=False)
    birthday = Column(Date, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)

# Create tables if they do not exist
Base.metadata.create_all(engine)