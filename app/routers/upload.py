# app/routers/upload.py
import hashlib
import io
import pandas as pd
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def calcular_hash(file_bytes: bytes) -> str:
    return hashlib.md5(file_bytes).hexdigest()

@router.post("/", tags=["Upload"])
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
            try:
                # Pular as duas primeiras linhas e garantir que a segunda linha seja usada como cabeçalho
                df = pd.read_csv(io.BytesIO(file_bytes), sep=";", header=1, encoding="utf-8", on_bad_lines="skip")
            except UnicodeDecodeError:
                df = pd.read_csv(io.BytesIO(file_bytes), sep=";", header=1, encoding="ISO-8859-1", on_bad_lines="skip")
        else:
            df = pd.read_excel(io.BytesIO(file_bytes), header=1)  # No Excel, usa a segunda linha como cabeçalho
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler o arquivo: {str(e)}")
    
    # Normaliza os nomes das colunas removendo espaços extras
    df.columns = df.columns.str.strip()

    # Validação e mapeamento dos dados
    expected_columns = {"RptDt", "TckrSymb"}
    if not expected_columns.issubset(set(df.columns)):
        raise HTTPException(status_code=400, detail=f"Arquivo não possui todas as colunas obrigatórias. Colunas encontradas: {list(df.columns)}")
    
    # Conversão dos dados e inserção no banco
    records = []
    for _, row in df.iterrows():
        try:
            # Tente converter RptDt para um objeto datetime
            rptdt = pd.to_datetime(row.get("RptDt"), errors='coerce')
            if pd.isna(rptdt):
                rptdt = None  # Ou defina uma data padrão, se necessário
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao converter a data 'RptDt': {str(e)}")
    
        try:
            record = models.Record(
                RptDt=rptdt,  # Atribuindo o valor convertido de RptDt
                TckrSymb=row.get("TckrSymb"),
                MktNm=row.get("MktNm"),
                SctyCtgyNm=row.get("SctyCtgyNm"),
                ISIN=row.get("ISIN"),
                CrpnNm=row.get("CrpnNm")
            )
            records.append(record)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao montar o registro: {str(e)}")

    # Tentando salvar os registros no banco de dados
    try:
        db.bulk_save_objects(records)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar no banco de dados: {str(e)}")

    return {"detail": "Arquivo processado com sucesso", "upload_id": upload_record.id}