from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    position = Column(String(50), nullable=False)


def create_database():
    try:
        engine = create_engine('mysql://username:password@localhost/db_name')
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"Error creating database: {e}")


def add_employee(name, age, position):
    try:
        if not (isinstance(name, str) and isinstance(age, int) and isinstance(position, str)):
            raise ValueError("Invalid input data types")

        if not (1 <= len(name) <= 50 and 1 <= len(position) <= 50):
            raise ValueError("Name and position must be between 1 and 50 characters")

        if not (18 <= age <= 65):
            raise ValueError("Age must be between 18 and 65")

        engine = create_engine('mysql://username:password@localhost/db_name')
        Session = sessionmaker(bind=engine)
        session = Session()

        new_employee = Employee(name=name, age=age, position=position)
        session.add(new_employee)
        session.commit()
        session.close()

    except ValueError as ve:
        print(f"Validation error: {ve}")
    except SQLAlchemyError as e:
        print(f"Error adding employee: {e}")


create_database()
add_employee("John Doe", 30, "Developer")