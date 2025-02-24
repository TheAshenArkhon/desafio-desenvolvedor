# app/routers/upload.py
import hashlib
import io
import pandas as pd
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def calcular_hash(file_bytes: bytes) -> str:
    return hashlib.md5(file_bytes).hexdigest()

@router.post("/upload", tags=["Upload"])
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Validação do tipo de arquivo
    if not file.filename.endswith((".csv", ".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Arquivo inválido. Utilize CSV ou Excel.")
    
    file_bytes = await file.read()
    file_hash = calcular_hash(file_bytes)
    
    # Verifica se o arquivo já foi enviado
    existing_file = db.query(models.UploadFile).filter(models.UploadFile.file_hash == file_hash).first()
    if existing_file:
        raise HTTPException(status_code=400, detail="Este arquivo já foi enviado.")
    
    # Salva o registro do upload
    upload_record = models.UploadFile(file_name=file.filename, file_hash=file_hash)
    db.add(upload_record)
    db.commit()
    db.refresh(upload_record)
    
    # Processa o arquivo e insere os registros
    try:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(file_bytes))
        else:
            df = pd.read_excel(io.BytesIO(file_bytes))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler o arquivo: {str(e)}")
    
    # Validação e mapeamento dos dados (adaptar conforme necessidade)
    expected_columns = {"RptDt", "TckrSymb", "MktNm", "SctyCtgyNm", "ISIN", "CrpnNm"}
    if not expected_columns.issubset(set(df.columns)):
        raise HTTPException(status_code=400, detail="Arquivo não possui todas as colunas obrigatórias.")
    
    # Conversão dos dados e inserção no banco
    records = []
    for _, row in df.iterrows():
        record = models.Record(
            RptDt=row["RptDt"],
            TckrSymb=row["TckrSymb"],
            MktNm=row["MktNm"],
            SctyCtgyNm=row["SctyCtgyNm"],
            ISIN=row["ISIN"],
            CrpnNm=row["CrpnNm"],
        )
        records.append(record)
    
    db.bulk_save_objects(records)
    db.commit()
    
    return {"detail": "Arquivo processado com sucesso", "upload_id": upload_record.id}
