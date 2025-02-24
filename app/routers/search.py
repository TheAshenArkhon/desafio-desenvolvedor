# app/routers/search.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from typing import Optional, List
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/search", tags=["Busca"])
def search_records(
    TckrSymb: Optional[str] = Query(None),
    RptDt: Optional[str] = Query(None),  # no formato YYYY-MM-DD
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(models.Record)
    
    if TckrSymb and RptDt:
        try:
            rpt_date = datetime.strptime(RptDt, "%Y-%m-%d").date()
        except Exception:
            raise HTTPException(status_code=400, detail="Formato de RptDt inválido. Utilize YYYY-MM-DD.")
        query = query.filter(models.Record.TckrSymb == TckrSymb, models.Record.RptDt == rpt_date)
    elif not TckrSymb and not RptDt:
        # Paginação quando não são enviados parâmetros
        query = query.offset((page - 1) * page_size).limit(page_size)
    else:
        # Se apenas um dos parâmetros for enviado, podemos decidir se a busca é permitida ou não
        raise HTTPException(status_code=400, detail="Envie ambos os parâmetros ou nenhum para paginação.")
    
    results = query.all()
    
    # Formata o retorno com os campos esperados
    response = []
    for r in results:
        response.append({
            "RptDt": r.RptDt.strftime("%Y-%m-%d"),
            "TckrSymb": r.TckrSymb,
            "MktNm": r.MktNm,
            "SctyCtgyNm": r.SctyCtgyNm,
            "ISIN": r.ISIN,
            "CrpnNm": r.CrpnNm
        })
    
    return response
