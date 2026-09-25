from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class PolicyLog(Base):
    __tablename__ = "policy_logs"

    id = Column(Integer, primary_key=True, index=True)
    parameter_name = Column(String, nullable=False)
    old_value = Column(String, nullable=True)
    new_value = Column(String, nullable=False)
    changed_by = Column(String, default="AI")
    changed_at = Column(DateTime(timezone=True), server_default=func.now())
