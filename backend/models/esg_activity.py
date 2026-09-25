from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from database import Base

class ESGActivity(Base):
    __tablename__ = "esg_activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=True)
    activity_type = Column(String, nullable=False)
    verification_method = Column(String, nullable=False)
    reward_amount = Column(Float, default=0.0)
    tx_hash = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
