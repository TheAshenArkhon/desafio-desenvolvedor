# app/models.py
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from app.database import Base

class UploadFile(Base):
    __tablename__ = "upload_files"
    
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, unique=True, index=True)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    file_hash = Column(String, unique=True)

class Record(Base):
    __tablename__ = "records"
    
    id = Column(Integer, primary_key=True, index=True)
    RptDt = Column(Date)
    TckrSymb = Column(String, index=True)
    MktNm = Column(String)
    SctyCtgyNm = Column(String)
    ISIN = Column(String)
    CrpnNm = Column(String)
