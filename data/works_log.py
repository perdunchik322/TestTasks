from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean


class Jobs(SqlAlchemyBase):
    __tablename__ = "works_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    names = Column(String, nullable=False)
    Duration = Column(String, nullable=False)
    list_of_collaborators = Column(String, nullable=False)
    if_finished = Column(String)
