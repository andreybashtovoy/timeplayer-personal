from sqlalchemy import Column, String, Integer, Sequence, Boolean, ForeignKey
from sqlalchemy.types import TIMESTAMP, Interval
from sqlalchemy.sql import func

from .loader import db


class User(db.Model):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(32))
    registration_datetime = Column(TIMESTAMP(), server_default=func.current_timestamp())


class Chat(db.Model):
    __tablename__ = "chats"
    chat_id = Column(Integer, primary_key=True)
    name = Column(String)


class ChatXUser(db.Model):
    __tablename__ = "chats_x_users"
    chat_id = Column(Integer, ForeignKey("chats.chat_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))


class ActivityType(db.Model):
    __tablename__ = "activity_types"
    id = Column(Integer, Sequence('activity_type_id_seq'), primary_key=True)
    name = Column(String(100))
    with_benefit = Column(Boolean, default=False)
    owner = Column(Integer, ForeignKey("users.user_id"))
    access = Column(Integer, default=0)


class Subactivity(db.Model):
    __tablename__ = "subactivities"
    id = Column(Integer, Sequence('subactivity_id_seq'), primary_key=True)
    activity_type = Column(Integer, ForeignKey('activity_types.id'))
    user_id = Column(Integer, ForeignKey("users.user_id"))


class Activity(db.Model):
    __tablename__ = "activities"
    id = Column(Integer, Sequence('activity_id_seq'), primary_key=True)
    activity_type = Column(Integer, ForeignKey('activity_types.id'))
    subactivity = Column(Integer, ForeignKey('subactivities.id'))
    start_time = Column(TIMESTAMP, server_default=func.current_timestamp())
    duration = Column(Interval)
    user_id = Column(Integer, ForeignKey("users.user_id"))



