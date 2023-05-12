from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import Session

# create a database instance
Base = declarative_base()

class UserActivity(Base):
    __tablename__ = "user_activity"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    activity_type = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
