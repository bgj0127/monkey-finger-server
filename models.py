from sqlalchemy import Column, Float, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


# 유저 모델 정의
class User(Base):
    __tablename__ = "user"

    user_id = Column(String, primary_key=True)
    user_pw = Column(String, nullable=False)
    register_date = Column(DateTime, nullable=False, default=datetime.now())
    typings = relationship("Typing")


# 타이핑 기록 모델 정의
class Typing(Base):
    __tablename__ = "typing"

    typing_id = Column(String, primary_key=True)
    wpm = Column(Float, nullable=False)
    acc = Column(Float, nullable=False)
    test_mode = Column(String, nullable=False)
    test_duration = Column(Float, nullable=False)
    language = Column(String, nullable=False)
    user_id = Column(String, ForeignKey("user.user_id"))
    timestamp = Column(BigInteger, nullable=False)
