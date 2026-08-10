from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database.connection import get_db, SessionLocal
from app.repositories.venda_repository import VendaRepository, init_db
from app.services.analytics_service import AnalyticsService

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        repo = VendaRepository(db)
        repo.carregar_e_popular_json("bdados_venda.json")
    finally:
        db.close()
    yield

app = FastAPI(
    title="Mercado 2 Irmãos - Analytics API",
    description="API REST e Dashboard de Business Intelligence para Mercado 2 Irmãos",
    version="1.0.0",
    lifespan=lifespan
)

@app.middleware("http")
def db_session_middleware(request, call_next):
    init_db()
    response = call_next(request)
    return response

@app.get("/", response_class=HTMLResponse)
def read_dashboard():
    with open("app/templates/dashboard.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/kpis")
def get_kpis(db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    return service.obter_resumo_kpis()

@app.get("/api/vendas-diarias")
def get_vendas_diarias(db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    return service.obter_vendas_diarias()

@app.get("/api/top-produtos")
def get_top_produtos(limit: int = 5, db: Session = Depends(get_db)):
    service = AnalyticsService(db)
    return service.obter_top_produtos_vendidos(limit=limit)

