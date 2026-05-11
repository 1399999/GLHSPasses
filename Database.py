from UI import UI 
from sqlalchemy import text, create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import MetaData, Table, Column, Integer

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    studentID: Mapped[int] = mapped_column(primary_key=True)
    timeElapsed: Mapped[int] = mapped_column()

    def __repr__(self):
        return f"User(id={self.studentID!r}), timeElapsed={self.timeElapsed!r}"

stmt= text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")

engine = create_engine('sqlite:///data.db')

metadata_obj = MetaData()

dataStruct = UI()
    
print(dataStruct.studentID)
print(dataStruct.timeElapsed)

user_table = Table(
    "user_account",
    metadata_obj,
    Column("studentID", Integer, primary_key=True),
    Column("timeElapsed", Integer)
)

metadata_obj.create_all(engine)

user = User(studentID=dataStruct.studentID, timeElapsed=dataStruct.timeElapsed)

with Session(engine) as session:
    session.add(user)
    session.commit()