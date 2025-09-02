from fastapi import FastAPI
from .database import Base, engine
from .routers import products

app = FastAPI(title="Estocka API")

# Cria as tabelas no Postgres (para começar; depois podemos migrar para Alembic)
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

# Rotas
app.include_router(products.router)
