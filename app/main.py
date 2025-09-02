from fastapi import FastAPI
from .database import Base, engine
from .routers import products
from .routers import products, movements


app = FastAPI(title="Estocka API")

# cria as tabelas (simples, por enquanto)
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

# routers
app.include_router(products.router)
app.include_router(movements.router)   # <-- ADICIONE ESTA LINHA
