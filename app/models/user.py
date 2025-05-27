from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users_config"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, comment="用户名")
    password_hash = Column(String(128), nullable=False, comment="加密后的密码")
    salt = Column(String(32), nullable=False, comment="加密用的盐")
    created_at = Column(TIMESTAMP, server_default=func.now())
