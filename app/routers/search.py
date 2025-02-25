from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from typing import Optional, List
from datetime import datetime

# Define a rota com um prefixo para evitar confusão
router = APIRouter(prefix="/search", tags=["Busca"])

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", tags=["Busca"])
def search_records(
    TckrSymb: Optional[str] = Query(None, description="Símbolo do ticker"),
    RptDt: Optional[str] = Query(None, description="Data do relatório no formato YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    """
    Busca registros no banco de dados com base no símbolo do ticker (`TckrSymb`) e na data do relatório (`RptDt`).

    - Ambos os filtros são opcionais, podendo ser usados separadamente ou juntos.
    - Se `RptDt` for enviado, ele deve estar no formato `YYYY-MM-DD`, caso contrário um erro 400 será retornado.
    """
    
    query = db.query(models.Record)

    # Filtro por TckrSymb, se fornecido
    if TckrSymb:
        query = query.filter(models.Record.TckrSymb == TckrSymb)
    
    # Filtro por RptDt, se fornecido
    if RptDt:
        try:
            rpt_date = datetime.strptime(RptDt, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de RptDt inválido. Utilize YYYY-MM-DD.")
        query = query.filter(models.Record.RptDt == rpt_date)
    
    # Executando a consulta
    results = query.all()

    # Se não houver resultados, retornamos um erro 404
    if not results:
        raise HTTPException(status_code=404, detail="Nenhum registro encontrado.")

    # Preparando a resposta
    response = []
    for r in results:
        response.append({
            "RptDt": r.RptDt.strftime("%Y-%m-%d") if r.RptDt else None,  # Adicionando verificação para evitar erro caso a data seja nula
            "TckrSymb": r.TckrSymb,
            "MktNm": r.MktNm,
            "SctyCtgyNm": r.SctyCtgyNm,
            "ISIN": r.ISIN,
            "CrpnNm": r.CrpnNm
        })

    return response


#            "RptDt": r.RptDt.strftime("%Y-%m-%d"),
#           "TckrSymb": r.TckrSymb,
#            "Asst": r.Asst,
#            "AsstDesc": r.AsstDesc,
#            "SgmtNm": r.SgmtNm,
#            "MktNm": r.MktNm,
#            "SctyCtgyNm": r.SctyCtgyNm,
#            "XprtnCd": r.XprtnCd,
#            "TradgStartDt": r.TradgStartDt,
#            "TradgEndDt": r.TradgEndDt,
#            "eCd": r.eCd,
#            "ConvsCritNm": r.ConvsCritNm,
#            "MtrtyDtTrgtPt": r.MtrtyDtTrgtPt,
#            "ReqrdConvsInd": r.ReqrdConvsInd,
#            "ISIN": r.ISIN,
#           "CFICd": r.CFICd,
#            "DlvryNtceStartDt": r.DlvryNtceStartDt,
#            "DlvryNtceEndDt": r.DlvryNtceEndDt,
#            "OptnTp": r.OptnTp,
#            "CtrctMltplr": r.CtrctMltplr
#            "CrpnNm": r.CrpnNm
