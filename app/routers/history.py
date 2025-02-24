# app/routers/history.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from typing import Optional
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", tags=["Histórico"])
def get_upload_history(
    file_name: Optional[str] = Query(None),
    reference_date: Optional[str] = Query(None),  # no formato YYYY-MM-DD
    db: Session = Depends(get_db)
):
    query = db.query(models.UploadFile)
    
    if file_name:
        query = query.filter(models.UploadFile.file_name.contains(file_name))
    if reference_date:
        try:
            ref_date = datetime.strptime(reference_date, "%Y-%m-%d")
            query = query.filter(models.UploadFile.upload_date.cast(models.UploadFile.upload_date.type.python_type) >= ref_date)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Data de referência inválida. Utilize o formato YYYY-MM-DD.")
    
    uploads = query.all()
    
    return uploads
