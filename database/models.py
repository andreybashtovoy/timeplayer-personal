from sqlalchemy import Column, String, Integer, Sequence, Boolean, ForeignKey
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql import func


from .loader import db


class User(db.Model):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(32))
    registration_datetime = Column(TIMESTAMP(), server_default=func.current_timestamp())


class ActivityType(db.Model):
    __tablename__ = "activity_types"
    id = Column(Integer, Sequence('activity_type_id_seq'), primary_key=True)
    name = Column(String(100))
    with_benefit = Column(Boolean, default=False)
    owner = Column(Integer, ForeignKey("users.user_id"))
    access = Column(Integer, default=0)
