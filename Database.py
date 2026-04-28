from UI import UI 
from sqlalchemy import text, create_engine, select
from sqlalchemy.orm import DeclarativeBase
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

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

metadata_obj = MetaData()

dataStruct = UI()
print(dataStruct.studentID)
print(dataStruct.timeElapsed)

user_table = Table(
    "user_account",
    metadata_obj,
    Column("student id", Integer, primary_key=True),
    Column("time elapsed", Integer)
)

metadata_obj.create_all(engine)

harveyWinstein = User(studentID=dataStruct.studentID, timeElapsed=dataStruct.timeElapsed)
user = User(studentID=dataStruct.studentID, timeElapsed=dataStruct.timeElapsed)

Base.metadata.create_all(engine)

stmt = select(user_table).where(user_table.c.name == "student id")

print(stmt)