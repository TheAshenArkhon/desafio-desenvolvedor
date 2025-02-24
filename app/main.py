# app/main.py
from fastapi import FastAPI
from app.routers import upload, history, search

app = FastAPI(
    title="Desafio Dev API",
    description= "Upload e Busca de Arquivos",
    version="1.0",
    docs_url="/docs",  # Certifique-se de que o Swagger UI está ativado
    redoc_url="/redoc",  # URL do Redoc
    openapi_url="/openapi.json"  # Especificação OpenAPI
    )

app.include_router(upload.router)
app.include_router(history.router)
app.include_router(search.router)
