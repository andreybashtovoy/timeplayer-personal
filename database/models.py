from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer


Base = declarative_base()


class A(Base):
    __tablename__ = "a"
    id = Column(Integer, primary_key=True)
    data = Column(String)
