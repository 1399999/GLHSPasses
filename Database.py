import time as time

## NEXT STEP USE FASTAPI TO CREATE AN API ENDPOINT TO RECEIVE THE DATA INSTEAD OF USING A UI CLASS TO SIMULATE THE DATA INPUT. 
## THIS WILL ALLOW FOR REAL-TIME DATA COLLECTION AND STORAGE IN THE DATABASE.

from decimal import *

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, relationship
from sqlalchemy import MetaData, ForeignKey, select

from sqlalchemy.orm import Mapped, joinedload
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    studentID: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)

    actions: Mapped[list["Action"]] = relationship(back_populates="user_rel", cascade="all, delete-orphan")

class Action(Base):
    __tablename__ = "action"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    location: Mapped[str] = mapped_column()
    user: Mapped[User] = mapped_column(ForeignKey(User.studentID))

    time: Mapped[float] = mapped_column(default=time.time)

    user_rel: Mapped["User"] = relationship(back_populates="actions")    

class DataBase():

    def __init__(self):
        self.engine = create_engine('sqlite:///data.db')
        
        metadata_obj = MetaData()

        Base.metadata.create_all(self.engine)
        metadata_obj.create_all(self.engine)

    def addAction(self, desiredID, desiredName, desiredLocation):
        with Session(self.engine) as session:
            db_user = session.scalar(
                select(User)
                .where(User.studentID == desiredID)
                .options(joinedload(User.actions))
            )

            if not db_user:
                db_user = User(
                    studentID = desiredID,
                    name = desiredName
                )

                session.add(db_user)

            db_user.actions.append(Action(location = desiredLocation))

            session.commit()
            session.refresh(db_user)

# searchID = int(input("Enter the student ID you want to search for: "))

# stmt = select(User).where(User.studentID == searchID).options(joinedload(User.actions))

# with Session(engine) as session:
#     db_user = session.scalar(stmt)

#     if db_user:
#         print(f"User Found as: {db_user.studentID} under name {db_user.name}")
#         print("Actions: ")
#         for action in db_user.actions:
#             print(f"Location: {action.location} at time {action.time}")