from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy import Column, Integer, String, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String)
    name = Column(String)
    age = Column(Integer)
    position = Column(String)
    speciality = Column(String)
    address = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    modified_date = Column(DateTime)
    jobs = orm.relationship("Jobs", back_populates="team_leader")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def repr(self):
        return f"<Colonist>{self.id}{self.surname}{self.name}"
