import time as time
import pandas as pd

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

    actions: Mapped[list["Action"]] = relationship(back_populates="user_rel", cascade="all, delete-orphan", order_by=lambda: Action.id)

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

    def addAction(self, desiredID, desiredLocation):
        with Session(self.engine) as session:
            db_user = session.scalar(
                select(User)
                .where(User.studentID == desiredID)
                .options(joinedload(User.actions))
            )

            if not db_user: return False

            db_user.actions.append(Action(location = desiredLocation))

            session.commit()
            session.refresh(db_user)

            return True

    def addUser(self, desiredID, desiredName):
        with Session(self.engine) as session:
            db_user = session.scalar(
                select(User)
                .where(User.studentID == desiredID)
                .options(joinedload(User.actions))
            )

            if db_user: return False

            try:
                new_user = User(studentID=desiredID, name=desiredName)
                session.add(new_user)
                session.commit()
                session.refresh(new_user)
            except:
                return False

            return True
        
    def replaceUsers(self, given_df):
        try:
            df = pd.read_csv(given_df)

            df = df.reset_index(drop=True)

            df.to_sql(
                "user", 
                self.engine, 
                if_exists="replace", 
                index=False,
                index_label="false"
            )
            return True
            
        except:
            return False

    def searchName(self, searchName):
        stmt = select(User).where(User.name == searchName).options(joinedload(User.actions))

        with Session(self.engine) as session:
            db_user = session.scalar(stmt)

            if db_user:
                actions = [[action.location, action.time] for action in db_user.actions]
                return [db_user.studentID, db_user.name, actions]
        
        return []
    
    def fetch(self):
        stmt = select(User).options(joinedload(User.actions))

        with Session(self.engine) as session:
            users = session.execute(stmt).unique().scalars().all()

        if users:
            user_data = [
                [action.id, action.location, user.name, action.time]
                
                for user in users
                for action in user.actions
            ]
            return user_data
        
        return []