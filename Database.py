from UI import UI

## NEXT STEP USE FASTAPI TO CREATE AN API ENDPOINT TO RECEIVE THE DATA INSTEAD OF USING A UI CLASS TO SIMULATE THE DATA INPUT. 
## THIS WILL ALLOW FOR REAL-TIME DATA COLLECTION AND STORAGE IN THE DATABASE.

from decimal import *

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, relationship
from sqlalchemy import MetaData, ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

engine = create_engine('sqlite:///data.db')

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    studentID: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    actions: Mapped[list["Action"]] = relationship(back_populates="user_rel")

class Action(Base):
    __tablename__ = "registry"

    id: Mapped[int] = mapped_column(primary_key=True)
    location: Mapped[str] = mapped_column()
    user: Mapped[User] = mapped_column(ForeignKey("user.studentID"))

    timeStart: Mapped[int] = mapped_column(nullable=True)
    timeEnd: Mapped[int] = mapped_column(nullable=True)

    user_rel: Mapped["User"] = relationship(back_populates="actions")

    def __init__(self, user: int, timeStart: datetime, location: str = None):
        self.location = location
        self.user = user


metadata_obj = MetaData()

dataStruct = UI()
    
print(dataStruct.studentID)
print(dataStruct.timeElapsed)

Base.metadata.create_all(engine)

metadata_obj.create_all(engine)

user = User(
        studentID=dataStruct.studentID, 
        timeElapsed=float(Decimal(dataStruct.timeElapsed).quantize(Decimal('0.001'))), 
        location=dataStruct.location
    )

with Session(engine) as session:
    session.add(user)
    session.commit()