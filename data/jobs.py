from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy_serializer import SerializerMixin


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_leader_id = Column(Integer, ForeignKey('users.id'))
    team_leader = orm.relationship("User", back_populates="jobs")
    job = Column(String)
    work_size = Column(Integer)
    collaborators = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_finished = Column(Boolean)
    serialize_rules = ('-team_leader.jobs',)
