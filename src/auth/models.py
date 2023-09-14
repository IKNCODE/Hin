from src.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, MetaData, Table, TIMESTAMP


class Role(Base):
    __tablename__ = 'role'

    role_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    descr = Column(String, nullable=True)


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False)
    education = Column(String)
    role = Column(Integer, ForeignKey("role.role_id"), nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_verified = Column(Boolean, nullable=False)
    is_superuser = Column(Boolean, nullable=False)
