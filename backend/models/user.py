from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    user_type = Column(Enum("citizen", "merchant", "admin", name="user_type"), default="citizen")
    algorand_address = Column(String, nullable=True)
    region = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
