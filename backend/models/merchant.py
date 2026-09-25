from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    store_name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    business_number = Column(String, nullable=True)
    esg_types = Column(String, nullable=True)
    qr_code = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
