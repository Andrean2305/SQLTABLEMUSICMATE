from sqlalchemy.orm import sessionmaker
from Models import Base,UserActivity
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.declarative import declarative_base



SQLALCHEMY_DATABASE_URL = "sqlite:///./ACT.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/create_table")
async def create_table(id_col: str, user_id_col: str, activity_type_col: str, created_at_col: str, db: Session = Depends(get_db)):
    try:
        # Define the table
        class NewTable(Base):
            __tablename__ = "Activity"
            
            id = Column(Integer, primary_key=True, index=True, name=id_col)
            user_id = Column(String, index=True, name=user_id_col)
            activity_type = Column(String, name=activity_type_col)
            created_at = Column(DateTime(timezone=True), server_default=func.now(), name=created_at_col)

        # Create the table
        Base.metadata.create_all(bind=engine, tables=[NewTable.__table__])
        
        return {"message": f"Table 'Activity' created successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

class Activity(Base):
    __tablename__ = 'Activity'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    activity_type = Column(String)
    created_at = Column(DateTime)

@app.get("/user_activity")
async def get_user_activity(db: Session = Depends(get_db)):
    try:
        activities = db.query(Activity).all()
        return [activity.__dict__ for activity in activities]
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))
