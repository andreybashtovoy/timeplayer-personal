from sqlalchemy import Column, String, Integer, Sequence, Boolean, ForeignKey, BigInteger
from sqlalchemy.types import TIMESTAMP, Interval
from sqlalchemy.sql import func

from datetime import datetime

from .loader import db


class User(db.Model):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(32))
    registration_datetime = Column(TIMESTAMP(), default=datetime.utcnow, nullable=False)


class Chat(db.Model):
    __tablename__ = "chats"
    chat_id = Column(BigInteger, primary_key=True)
    name = Column(String)


class ChatXUser(db.Model):
    __tablename__ = "chats_x_users"
    chat_id = Column(BigInteger, ForeignKey("chats.chat_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))


class ActivityType(db.Model):
    __tablename__ = "activity_types"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    with_benefit_default = Column(Boolean, default=False, nullable=False)
    default = Column(Boolean, default=False, nullable=False)


class Subactivity(db.Model):
    __tablename__ = "subactivities"
    id = Column(Integer, Sequence('subactivities_id_seq'), primary_key=True)
    activity_type = Column(Integer, ForeignKey('activity_types.id'))
    user_id = Column(Integer, ForeignKey("users.user_id"))


class Activity(db.Model):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)
    activity_type = Column(Integer, ForeignKey('activity_types.id'), nullable=False)
    subactivity = Column(Integer, ForeignKey('subactivities.id'))
    start_time = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    duration = Column(Interval)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    chat_id = Column(BigInteger, ForeignKey("chats.chat_id"), nullable=False)


class ChatXActivityType(db.Model):
    __tablename__ = "chats_x_activity_types"
    chat_id = Column(BigInteger, ForeignKey("chats.chat_id"), nullable=False)
    activity_type = Column(Integer, ForeignKey('activity_types.id'), nullable=False)
    with_benefit = Column(Boolean, default=False, nullable=False)
