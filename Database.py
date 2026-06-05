import time as time
import pandas as pd

from decimal import *

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, relationship
from sqlalchemy import MetaData, ForeignKey, select
from sqlalchemy.orm import Mapped, joinedload
from sqlalchemy.orm import mapped_column

from werkzeug.security import generate_password_hash, check_password_hash


class Base(DeclarativeBase):
    pass


class LoginUser(Base):
    __tablename__ = "login_user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(default="user")


class User(Base):
    __tablename__ = "user"

    studentID: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)

    actions: Mapped[list["Action"]] = relationship(
        back_populates="user_rel",
        cascade="all, delete-orphan",
        order_by=lambda: Action.id,
    )


class Action(Base):
    __tablename__ = "action"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    location: Mapped[str] = mapped_column()
    user: Mapped[User] = mapped_column(ForeignKey(User.studentID))
    time: Mapped[float] = mapped_column(default=time.time)

    user_rel: Mapped["User"] = relationship(back_populates="actions")


class DataBase():

    def __init__(self):
        self.engine = create_engine("sqlite:///data.db")
        metadata_obj = MetaData()
        Base.metadata.create_all(self.engine)
        metadata_obj.create_all(self.engine)

    def createLoginUser(self, username: str, password: str, role: str = "user") -> bool:
        """Create a new login account. Returns False if username already exists."""
        with Session(self.engine) as session:
            existing = session.scalar(
                select(LoginUser).where(LoginUser.username == username)
            )
            if existing:
                return False
            session.add(
                LoginUser(
                    username=username,
                    password_hash=generate_password_hash(password),
                    role=role,
                )
            )
            session.commit()
            return True

    def validateLogin(self, username: str, password: str):

        with Session(self.engine) as session:
            login_user = session.scalar(
                select(LoginUser).where(LoginUser.username == username)
            )
            if login_user and check_password_hash(login_user.password_hash, password):
                return {
                    "id": login_user.id,
                    "username": login_user.username,
                    "role": login_user.role,
                }
        return None

    def loginUserExists(self) -> bool:

        with Session(self.engine) as session:
            return session.scalar(select(LoginUser)) is not None

    def addAction(self, desiredID, desiredLocation):
        with Session(self.engine) as session:
            db_user = session.scalar(
                select(User)
                .where(User.studentID == desiredID)
                .options(joinedload(User.actions))
            )
            if not db_user:
                return False
            db_user.actions.append(Action(location=desiredLocation))
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
            if db_user:
                return False
            try:
                new_user = User(studentID=desiredID, name=desiredName)
                session.add(new_user)
                session.commit()
                session.refresh(new_user)
            except Exception:
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
                index_label="false",
            )
            return True
        except Exception:
            return False

    def searchName(self, searchName):
        stmt = (
            select(User)
            .where(User.name == searchName)
            .options(joinedload(User.actions))
        )
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
            return [
                [action.id, action.location, user.name, action.time]
                for user in users
                for action in user.actions
            ]
        return []
