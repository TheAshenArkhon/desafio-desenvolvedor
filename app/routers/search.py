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

@router.get("/", tags=["Busca"])
def search_records(
    TckrSymb: Optional[str] = Query(None),
    RptDt: Optional[str] = Query(None),  # no formato YYYY-MM-DD
    db: Session = Depends(get_db)
):
    query = db.query(models.Record)
    
    if TckrSymb and RptDt:
        try:
            rpt_date = datetime.strptime(RptDt, "%Y-%m-%d").date()
        except Exception:
            raise HTTPException(status_code=400, detail="Formato de RptDt inválido. Utilize YYYY-MM-DD.")
        query = query.filter(models.Record.TckrSymb == TckrSymb, models.Record.RptDt == rpt_date)
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
#            "Asst": r.Asst,
#            "AsstDesc": r.AsstDesc,
#            "SgmtNm": r.SgmtNm,
            "MktNm": r.MktNm,
            "SctyCtgyNm": r.SctyCtgyNm,
#            "XprtnCd": r.XprtnCd,
#            "TradgStartDt": r.TradgStartDt,
#            "TradgEndDt": r.TradgEndDt,
#            "eCd": r.eCd,
#            "ConvsCritNm": r.ConvsCritNm,
#            "MtrtyDtTrgtPt": r.MtrtyDtTrgtPt,
#            "ReqrdConvsInd": r.ReqrdConvsInd,
            "ISIN": r.ISIN,
#           "CFICd": r.CFICd,
#            "DlvryNtceStartDt": r.DlvryNtceStartDt,
#            "DlvryNtceEndDt": r.DlvryNtceEndDt,
#            "OptnTp": r.OptnTp,
#            "CtrctMltplr": r.CtrctMltplr
            "CrpnNm": r.CrpnNm
        })
    
    return response
