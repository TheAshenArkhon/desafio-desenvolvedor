# app/main.py
from fastapi import FastAPI
from app.routers import upload, history, search
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Desafio Dev API",
    description= "Upload e Busca de Arquivos",
    version="1.0",
    docs_url="/docs",  # Certifique-se de que o Swagger UI está ativado
    redoc_url="/redoc",  # URL do Redoc
    openapi_url="/openapi.json"  # Especificação OpenAPI
    )

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite chamadas de qualquer domínio (ajuste para produção)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(history.router, prefix="/history", tags=["Histórico"])
app.include_router(search.router, prefix="/search", tags=["Busca"])

@app.get("/")
def read_root():
    return {"message": "API funcionando! use /docs no url para acessar a documentação."}


# Para rodar a aplicação, execute o comando abaixo:
# python -m uvicorn app.main:app --reload