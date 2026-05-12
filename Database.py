from UI import UI

## NEXT STEP USE FASTAPI TO CREATE AN API ENDPOINT TO RECEIVE THE DATA INSTEAD OF USING A UI CLASS TO SIMULATE THE DATA INPUT. 
## THIS WILL ALLOW FOR REAL-TIME DATA COLLECTION AND STORAGE IN THE DATABASE.

from decimal import *

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import MetaData, Table, Column, Integer, String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    studentID: Mapped[int] = mapped_column(primary_key=True)
    timeElapsed: Mapped[int] = mapped_column()
    location: Mapped[str] = mapped_column(nullable=True)

engine = create_engine('sqlite:///data.db')

metadata_obj = MetaData()

dataStruct = UI()
    
print(dataStruct.studentID)
print(dataStruct.timeElapsed)

user_table = Table(
    "user_account",
    metadata_obj,
    Column("studentID", Integer, primary_key=True),
    Column("timeElapsed", Integer),
    Column("location", String, nullable=True)
)

metadata_obj.create_all(engine)

user = User(
        studentID=dataStruct.studentID, 
        timeElapsed=float(Decimal(dataStruct.timeElapsed).quantize(Decimal('0.001'))), 
        location=dataStruct.location
    )


with Session(engine) as session:
    session.add(user)
    session.commit()